from fastapi import APIRouter, HTTPException
from app.services.camera_service import CameraService
from app.services.ai_service import AIService
from app.services.frontend_service import FrontendService
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/api", tags=["camera"])

@router.post("/pictures")
def capture_and_process():
    """
    프론트엔드 요청 API
    
    동작 순서:
    1. 라즈베리파이 카메라로 사진 촬영
    2. AI 서버로 이미지 전송 및 분석 결과 수신
    3. 프론트엔드로 결과 반환
    """
    try:
        logger.info("프론트엔드로부터 촬영 요청 수신")
        
        # 1. 이미지 촬영
        image_path = CameraService.capture_image()
        
        # 2. AI 서버로 전송 및 분석
        ai_response = AIService.send_image(image_path)
        
        # 3. 프론트엔드로 콜백
        # FrontendService.send_result(ai_response)
        
        logger.info(f"처리 완료 - 카테고리: {ai_response.get('category')}")
        
        # 4. 프론트엔드로 직접 응답 반환
        return {
            "success": True,
            "message": "이미지 촬영 및 분석 완료",
            "category": ai_response.get("category"),
            "ai_result": ai_response
        }
        
    except Exception as e:
        logger.error(f"API 처리 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    """서버 상태 확인용 API"""
    logger.info("헬스 체크 요청")
    return {
        "status": "healthy",
        "message": "Raspberry Pi Camera Server 작동중"
    }

@router.post("/test/capture")
def test_capture():
    """테스트용 간단한 촬영 API"""
    try:
        logger.info("테스트 촬영 요청")
        image_path = CameraService.capture_image()
        
        return {
            "success": True,
            "message": "테스트 촬영 완료",
            "image_path": image_path
        }
    except Exception as e:
        logger.error(f"테스트 촬영 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
