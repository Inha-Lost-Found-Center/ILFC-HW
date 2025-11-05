import os
from dotenv import load_dotenv

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
    
    @staticmethod
    def init_app():
        """애플리케이션 시작 시 필요한 초기화"""
        print(f"DEBUG: SAVE_DIR = {Config.SAVE_DIR}")
        print(f"DEBUG: AI_SERVER_URL = {Config.AI_SERVER_URL}")
        print(f"DEBUG: HOST = {Config.HOST}")
        print(f"DEBUG: PORT = {Config.PORT}")
        os.makedirs(Config.SAVE_DIR, exist_ok=True)
        
        if not Config.AI_SERVER_URL:
            raise ValueError("AI_SERVER_URL이 .env 파일에 설정되어 있지 않습니다!")
    
    @staticmethod
    def get_summary():
        """설정 정보 출력 (디버깅용)"""
        return {
            "save_dir": Config.SAVE_DIR,
            "ai_server": Config.AI_SERVER_URL,
            "frontend_callback": Config.FRONTEND_URL,
            "host": Config.HOST,
            "port": Config.PORT
        }
