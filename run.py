import uvicorn
from app.main import app
from app.config import Config
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

if __name__ == "__main__":
    logger.info(f"FastAPI 서버 시작: http://{Config.HOST}:{Config.PORT}")
    logger.info(f"API 문서: http://{Config.HOST}:{Config.PORT}/docs")
    

    uvicorn.run(
        "app.main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=False
    )
