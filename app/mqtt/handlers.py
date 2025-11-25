from app.services.camera_service import CameraService
from app.services.ai_service import AIService
from app.services.frontend_service import FrontendService
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

def handle_message(payload: dict):
    """
    AWS IoT Core → MQTT 메시지 수신 시 실행되는 메인 핸들러
    """
    command = payload.get("command")

    if command == "capture":
        return process_capture_workflow()

    logger.warning(f"알 수 없는 command: {command}")

def process_capture_workflow():
    """기존 FastAPI 기능 그대로 가져옴"""
    logger.info("MQTT: 촬영 요청 수신")

    image_path = CameraService.capture_image()
    ai_response = AIService.send_image(image_path)
    FrontendService.send_result(ai_response)

    logger.info(f"MQTT 처리 완료: {ai_response.get('category')}")
