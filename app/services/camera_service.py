import os
import subprocess
from datetime import datetime
from app.config import Config
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

class CameraService:
    """라즈베리파이 카메라 제어 서비스"""
    
    @staticmethod
    def capture_image():
        """라즈베리파이 카메라로 이미지 촬영"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(Config.SAVE_DIR, f"picture_{timestamp}.jpg")
        
        try:
            logger.info("이미지 촬영 시작")
            subprocess.run(
                ["rpicam-still", "-o", image_path, "-t", "1000"],
                check=True
            )
            logger.info(f"이미지 촬영 완료: {image_path}")
            return image_path
        except subprocess.CalledProcessError as e:
            logger.error(f"카메라 촬영 실패: {e}")
            raise Exception(f"카메라 촬영 실패: {str(e)}")
