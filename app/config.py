import os
from dotenv import load_dotenv
from app.utils.logger_config import setup_logger

load_dotenv()

class Config:
    """애플리케이션 전체 설정"""
    
    # 이미지 저장 디렉토리
    SAVE_DIR = os.getenv("SAVE_DIR")
    
    # AI 서버 URL
    AI_SERVER_URL = os.getenv("AI_SERVER_URL")
    
    # 프론트엔드 콜백
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    
    # 서버 호스트/포트
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    
    # 타임아웃 설정 (초)
    AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", 20))
    FRONTEND_TIMEOUT = int(os.getenv("FRONTEND_TIMEOUT", 10))

    # 카메라 연결 오류로 인해 테스트용 코드
    USE_MOCK_CAMERA = os.getenv("USE_MOCK_CAMERA", "false").lower() == "true"
    
    # 로거 초기화
    logger = setup_logger(__name__)

    @staticmethod
    def init_app():
        """애플리케이션 시작 시 필요한 초기화"""
        Config.logger.info("=== Config 초기화 ===")
        Config.logger.info(f"SAVE_DIR = {Config.SAVE_DIR}")
        Config.logger.info(f"AI_SERVER_URL = {Config.AI_SERVER_URL}")
        Config.logger.info(f"FRONTEND_URL = {Config.FRONTEND_URL}")
        Config.logger.info(f"HOST = {Config.HOST}")
        Config.logger.info(f"PORT = {Config.PORT}")
        Config.logger.info(f"USE_MOCK_CAMERA = {Config.USE_MOCK_CAMERA}")
        os.makedirs(Config.SAVE_DIR, exist_ok=True)
        
        if not Config.AI_SERVER_URL:
            Config.logger.error("AI_SERVER_URL이 .env 파일에 설정되어 있지 않습니다.")
            raise ValueError("AI_SERVER_URL이 .env 파일에 설정되어 있지 않습니다.")

        Config.logger.info("Config 초기화 성공.\n")
    
    @staticmethod
    def get_summary():
        """설정 정보 출력 (디버깅용)"""
        return {
            "save_dir": Config.SAVE_DIR,
            "ai_server": Config.AI_SERVER_URL,
            "frontend_callback": Config.FRONTEND_URL,
            "host": Config.HOST,
            "port": Config.PORT,
            "use_mock_camera": Config.USE_MOCK_CAMERA
        }
