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
        
        # 카메라 연결 오류로 인해 Test 코드
        if Config.USE_MOCK_CAMERA:
            mock_image_path = os.path.join(Config.SAVE_DIR, "test_image.jpg")
            if not os.path.exists(mock_image_path):
                logger.error(f"MOCK 이미지 파일이 존재하지 않습니다: {mock_image_path}")
                raise FileNotFoundError(f"MOCK 이미지 {mock_image_path} 없음")
            
            logger.warning(f"MOCK 모드 활성화 - 실제 촬영 대신 {mock_image_path} 사용")
            return mock_image_path


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
