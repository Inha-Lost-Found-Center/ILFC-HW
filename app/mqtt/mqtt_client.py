import json
import ssl
import paho.mqtt.client as mqtt
from app.mqtt.handlers import handle_message
from app.config import Config
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

def on_connect(client, userdata, flags, rc):
    """MQTT 브로커 연결 성공 시 호출"""
    if rc == 0:
        logger.info(f"✅ MQTT 연결 성공 (rc={rc})")
        
        # 구독 시작
        subscribe_topic = f"locker/register/{Config.DEVICE_NAME}"
        client.subscribe(subscribe_topic, qos=1)
        logger.info(f"📡 구독 시작: {subscribe_topic}")
    else:
        logger.error(f"❌ MQTT 연결 실패 (rc={rc})")

def on_message(client, userdata, msg):
    """메시지 수신 시 호출"""
    logger.info(f"📨 [MQTT 수신] Topic: {msg.topic}")
    
    try:
        payload = json.loads(msg.payload.decode())
        logger.info(f"📦 Payload: {payload}")
        
        # 핸들러 호출 (client 객체 전달)
        handle_message(payload, client)
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON 파싱 오류: {e}")
    except Exception as e:
        logger.error(f"❌ MQTT 처리 오류: {e}", exc_info=True)

def on_disconnect(client, userdata, rc):
    """연결 끊김 시 호출"""
    logger.warning(f"⚠️ MQTT 연결 끊김 (rc={rc})")

def on_publish(client, userdata, mid):
    """메시지 발행 완료 시 호출"""
    logger.info(f"📤 메시지 발행 완료 (mid={mid})")

def start_mqtt():
    """MQTT 클라이언트 시작"""
    logger.info("🚀 MQTT 클라이언트 초기화 중...")
    
    # Client ID 설정 (팀원 자료에서는 CLIENT_NAME 사용)
    client = mqtt.Client(client_id=Config.CLIENT_NAME)
    
    # TLS 설정
    try:
        client.tls_set(
            ca_certs=Config.AWS_ROOT_CA,
            certfile=Config.AWS_CERT,
            keyfile=Config.AWS_PRIVATE_KEY,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        logger.info("🔐 TLS 설정 완료")
    except Exception as e:
        logger.error(f"❌ TLS 설정 실패: {e}")
        raise
    
    # 콜백 함수 등록
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    
    # 연결
    try:
        logger.info(f"🔌 MQTT 브로커 연결 시도: {Config.MQTT_HOST}:8883")
        client.connect(Config.MQTT_HOST, 8883, keepalive=60)
        
        logger.info("🔄 MQTT 루프 시작 (Ctrl+C로 종료)")
        client.loop_forever()
        
    except KeyboardInterrupt:
        logger.info("⏹️ 사용자에 의해 종료됨")
        client.disconnect()
    except Exception as e:
        logger.critical(f"❌ MQTT 연결 실패: {e}", exc_info=True)
        raise