import requests
from app.config import Config
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

class FrontendService:
    """프론트엔드와의 통신 서비스"""
    
    @staticmethod
    def send_result(ai_response: dict):
        """
        AI 분석 결과를 프론트엔드로 전송
        
        Args:
            ai_response: AI 서버로부터 받은 분석 결과
        """
        if not Config.FRONTEND_URL:
            logger.info("FRONTEND_URL이 설정되지 않아 프론트엔드 전송 생략")
            return
        
        try:
            logger.info(f"프론트엔드로 결과 전송: {Config.FRONTEND_URL}")
            response = requests.post(
                Config.FRONTEND_URL,
                json=ai_response,
                timeout=Config.FRONTEND_TIMEOUT
            )
            logger.info(f"프론트엔드 전송 완료: {response.status_code}")
            
            if response.status_code != 200:
                logger.warning(f"프론트엔드 응답 오류: {response.text}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"프론트엔드 요청 중 예외 발생: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"프론트엔드 전송 실패: {e}", exc_info=True)
