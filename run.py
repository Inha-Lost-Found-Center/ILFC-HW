import uvicorn
from app.main import app
from app.config import Config
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

if __name__ == "__main__":
    try:
        # 설정 초기화
        Config.init_app()
        
        logger.info("=" * 50)
        logger.info("🚀 라즈베리파이 MQTT 클라이언트 시작")
        logger.info("=" * 50)
        
        # MQTT 클라이언트 시작 (블로킹)
        start_mqtt()
        
    except KeyboardInterrupt:
        logger.info("\n👋 프로그램 종료")
    except Exception as e:
        logger.critical(f"❌ 프로그램 실행 실패: {e}", exc_info=True)

# if __name__ == "__main__":
#     logger.info(f"FastAPI 서버 시작: http://{Config.HOST}:{Config.PORT}")
#     logger.info(f"API 문서: http://{Config.HOST}:{Config.PORT}/docs")
    

#     uvicorn.run(
#         "app.main:app",
#         host=Config.HOST,
#         port=Config.PORT,
#         reload=False
#     )
