import os
import subprocess
import requests
from datetime import datetime
from dotenv import load_dotenv
from logger_config import setup_logger

logger = setup_logger()
load_dotenv()

SAVE_DIR = os.getenv("SAVE_DIR")
AI_SERVER_URL = os.getenv("AI_SERVER_URL")

os.makedirs(SAVE_DIR, exist_ok=True)

def capture_image():
    """라즈베리파이 카메라로 이미지 촬영"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(SAVE_DIR, f"picture_{timestamp}.jpg")

    try:
        subprocess.run(
            ["rpicam-still", "-o", image_path, "-t", "1000"],
            check=True
        )
        logger.info(f"이미지 촬영 완료: {image_path}")
        return image_path
    except subprocess.CalledProcessError as e:
        logger.error(f"카메라 촬영 실패: {e}")
        raise

def send_image(image_path: str):
    """이미지를 AI 서버로 전송하고 응답 처리"""
    if not AI_SERVER_URL:
        logger.critical(".env 파일에 AI_SERVER_URL이 설정되어 있지 않습니다.")
        return

    logger.info(f"AI 서버로 이미지 전송 시작: {AI_SERVER_URL}")

    try:
        with open(image_path, "rb") as f:
            image_binary = f.read()

        headers = {
            "Content-Type": "image/jpeg"
        }

        response = requests.post(
            AI_SERVER_URL,
            headers=headers,
            data=image_binary,   # multipart 아님 — raw binary 직접 전송
            timeout=20
        )

        logger.info(f"응답 코드: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                category = data.get("category")
                if category:
                    logger.info(f"AI 분석 결과: {category}")
                else:
                    logger.warning("응답에 'category' 필드가 없습니다.")
            except Exception as e:
                logger.error(f"JSON 파싱 오류: {e}")
                logger.debug(f"응답 본문: {response.text}")
        else:
            logger.error(f"서버 전송 오류: HTTP {response.status_code}")
            logger.debug(f"응답 헤더: {response.headers}")
            logger.debug(f"응답 본문: {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"서버 요청 중 예외 발생: {e}", exc_info=True)
    except Exception as e:
        logger.critical(f"예상치 못한 오류 발생: {e}", exc_info=True)


def main():
    try:
        image_path = capture_image()
        send_image(image_path)
    except Exception as e:
        logger.critical(f"프로그램 실행 중 치명적 오류 발생: {e}")
    finally:
        logger.info("프로그램 종료")

if __name__ == "__main__":
    main()
