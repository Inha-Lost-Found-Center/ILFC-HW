import json
import time
from app.services.camera_service import CameraService
from app.services.ai_service import AIService
from app.utils.logger_config import setup_logger
from app.hardware.conveyor import ConveyorBelt

logger = setup_logger(__name__)

def handle_message(payload: dict, client):
    """
    AWS IoT Core → MQTT 메시지 수신 시 실행되는 메인 핸들러
    """
    action = payload.get("action")
    device_name = payload.get("device_name")
    
    logger.info(f"📩 메시지 수신 - action: {action}, device: {device_name}")

    if action == "REQUEST_REGISTER":
        return process_register_workflow(payload, client)
    
    logger.warning(f"알 수 없는 action: {action}")

def process_register_workflow(payload: dict, client):
    """
    분실물 등록 워크플로우
    1. 사진 촬영
    2. AI 분석 요청
    3. 하드웨어 제어 (컨베이어/액추에이터)
    4. 결과 보고 (MQTT Publish) -> 얘기 필요
    """
    logger.info("🔄 분실물 등록 프로세스 시작")
    
    try:
        # 1. 이미지 촬영
        logger.info("📸 카메라 촬영 시작")
        image_path = CameraService.capture_image()
        
        # 2. AI 서버로 전송 및 분석
        logger.info("🧠 AI 분석 요청")
        ai_response = AIService.send_image(image_path)
        category = ai_response.get("category")
        
        # 3. 하드웨어 제어
        logger.info(f"⚙️ 하드웨어 제어 시작 - 카테고리: {category}")
        control_hardware(category)
        
        # # 4. 결과 보고 (MQTT Publish)
        # result_payload = {
        #     "status": "success",
        #     "device_name": payload.get("device_name"),
        #     "category": category,
        #     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        #     "ai_result": ai_response
        # }
        
        # # 결과 토픽으로 publish
        # from app.config import Config
        # result_topic = f"locker/register/result/{Config.DEVICE_NAME}"
        # client.publish(result_topic, json.dumps(result_payload), qos=1)
        
        logger.info(f"✅ 처리 완료 - 카테고리: {category}")
        
    except Exception as e:
        logger.error(f"❌ 처리 중 오류 발생: {e}", exc_info=True)
        
        # 에러 보고
        error_payload = {
            "status": "error",
            "device_name": payload.get("device_name"),
            "error": str(e),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        from app.config import Config
        result_topic = f"locker/register/result/{Config.DEVICE_NAME}"
        client.publish(result_topic, json.dumps(error_payload), qos=1)

def control_hardware(category: str):
    """
    카테고리에 따라 컨베이어 벨트와 액추에이터 제어
    TODO: 실제 GPIO 제어 코드로 교체 필요
    """
    try:
        logger.info("⚙️ 컨베이어 벨트 초기화")
        ConveyorBelt.initialize()
      
        logger.info(f"⚙️ 컨베이어 벨트 가동 시작")
        ConveyorBelt.enable()
        logger.info(f"➡️ 컨베이어 벨트 정방향 이동 중...")
        ConveyorBelt.move_forward()
        
        logger.info(f"🦾 '{category}' 분류를 위해 액추에이터 작동")
        # activate_actuator(category)
        
        time.sleep(1)
        
        logger.info(f"⚙️ 컨베이어 벨트 정지")
        ConveyorBelt.disable()
    
    except Exception as e:
        logger.error(f"❌ 하드웨어 제어 실패: {e}", exc_info=True)
        # 에러 발생 시 안전하게 정지
        try:
            ConveyorBelt.disable()
        except:
            pass
        raise