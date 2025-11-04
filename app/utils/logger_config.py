import logging
import os
from dotenv import load_dotenv

load_dotenv()

def setup_logger(name: str = __name__) -> logging.Logger:
    """
    공통 로거 설정 모듈
    
    Args:
        name: 로거 이름 (항상 __name__을 전달)
    
    Returns:
        설정된 Logger 객체
    
    사용 예시:
        from app.utils.logger_config import setup_logger
        logger = setup_logger(__name__)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 이미 핸들러가 있으면 중복 추가 방지
    if logger.handlers:
        return logger

    # 로그 포맷 (로거 이름을 포함)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 파일 핸들러 (환경변수로 제어)
    enable_file_logging = os.getenv("ENABLE_FILE_LOGGING", "false").lower() == "true"
    
    if enable_file_logging:
        log_dir = os.getenv("LOG_DIR", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "app.log")
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
