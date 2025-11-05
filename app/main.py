from fastapi import FastAPI
from app.config import Config
from app.routes.camera_routes import router as camera_router
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

def create_app() -> FastAPI:
    """FastAPI 애플리케이션 팩토리"""
    
    # FastAPI 인스턴스 생성
    app = FastAPI(
        title="Raspberry Pi Camera API",
        description="라즈베리파이 카메라 촬영 및 AI 분석 API",
        version="1.0.0"
    )
    
    # 설정 초기화
    Config.init_app()
    logger.info("설정 초기화 완료")
    logger.info(f"설정 정보: {Config.get_summary()}")
    
    # 라우터 등록
    app.include_router(camera_router)
    logger.info("라우터 등록 완료")
    
    logger.info("FastAPI 애플리케이션 초기화 완료")
    
    return app

app = create_app()
