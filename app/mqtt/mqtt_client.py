import json
import paho.mqtt.client as mqtt
from app.mqtt.handlers import handle_message
from app.config import Config
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

def on_connect(client, userdata, flags, rc):
    logger.info(f"MQTT 연결 성공 rc={rc}")
    client.subscribe(Config.MQTT_TOPIC)

def on_message(client, userdata, msg):
    logger.info(f"[MQTT 수신] Topic={msg.topic}")
    try:
        payload = json.loads(msg.payload.decode())
        handle_message(payload)
    except Exception as e:
        logger.error(f"MQTT 처리 오류: {e}")

def start_mqtt():
    client = mqtt.Client()
    client.tls_set(
        Config.AWS_ROOT_CA,
        Config.AWS_CERT,
        Config.AWS_PRIVATE_KEY,
    )
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(Config.MQTT_HOST, 8883)
    client.loop_forever()
