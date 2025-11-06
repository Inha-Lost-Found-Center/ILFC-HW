import requests
from app.config import Config
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

class AIService:
    """AI 서버와의 통신 서비스"""
    
    @staticmethod
    def send_image(image_path: str):
        """
        이미지를 AI 서버로 전송하고 분석 결과 수신
        
        Args:
            image_path: 전송할 이미지 파일 경로
        
        Returns:
            dict: AI 서버의 분석 결과 (category 포함)
        """
        if not Config.AI_SERVER_URL:
            logger.critical("AI_SERVER_URL이 설정되어 있지 않습니다.")
            raise ValueError("AI_SERVER_URL이 설정되지 않았습니다.")
        
        logger.info(f"AI 서버로 이미지 전송 시작: {Config.AI_SERVER_URL}")
        
        try:
            # 이미지 파일 읽기
            with open(image_path, "rb") as f:
                image_binary = f.read()
            
            # HTTP POST 요청 (raw binary 전송)
            response = requests.post(
                Config.AI_SERVER_URL,
                headers={"Content-Type": "image/jpeg"},
                data=image_binary,
                timeout=Config.AI_TIMEOUT
            )
            
            logger.info(f"AI 서버 응답 코드: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                category = data.get("category")
                
                if category:
                    logger.info(f"AI 분석 결과: {category}")
                    return data
                else:
                    logger.warning("응답에 'category' 필드가 없습니다.")
                    raise ValueError("AI 서버 응답에 category가 없습니다.")
            else:
                logger.error(f"AI 서버 오류: HTTP {response.status_code}")
                logger.debug(f"응답 본문: {response.text}")
                raise Exception(f"AI 서버 오류: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"AI 서버 요청 중 예외 발생: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.critical(f"예상치 못한 오류: {e}", exc_info=True)
            raise
