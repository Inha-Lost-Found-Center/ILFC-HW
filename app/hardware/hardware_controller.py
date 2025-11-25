"""
하드웨어 통합 제어 모듈
컨베이어 벨트 + 액추에이터를 조합한 워크플로우
"""
import time
from app.hardware.conveyor import ConveyorBelt
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)


class HardwareController:
    """하드웨어 통합 제어 클래스"""
    
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """모든 하드웨어 초기화"""
        if cls._initialized:
            logger.warning("HardwareController가 이미 초기화되어 있습니다.")
            return
        
        try:
            logger.info("하드웨어 초기화 시작...")
            
            ConveyorBelt.initialize()
            
            cls._initialized = True
            logger.info("모든 하드웨어 초기화 완료")
            
        except Exception as e:
            logger.error(f"하드웨어 초기화 실패: {e}")
            raise
    
    @classmethod
    def cleanup(cls):
        """모든 하드웨어 정리"""
        if cls._initialized:
            logger.info("하드웨어 정리 중...")
            ConveyorBelt.cleanup()
            cls._initialized = False
            logger.info("하드웨어 정리 완료")
    
    @classmethod
    def process_item(cls, category: str):
        """
        물건 처리 전체 워크플로우
        
        단계:
        1. 컨베이어 벨트 활성화
        2. 정방향 이동 (물건을 액추에이터 위치로)
        3. 대기 (물건 안착)
        4. 카테고리에 따라 액추에이터 작동
        5. 컨베이어 벨트 비활성화
        
        Args:
            category: AI가 분류한 카테고리
        """
        if not cls._initialized:
            raise RuntimeError("HardwareController가 초기화되지 않았습니다.")
        
        logger.info(f"물건 처리 시작 - 카테고리: {category}")
        logger.info("=" * 60)
        
        try:
            # Step 1: 컨베이어 벨트 활성화 및 이동
            logger.info("Step 1: 컨베이어 벨트 가동")
            ConveyorBelt.enable()
            ConveyorBelt.move_forward()
            
            # Step 2: 물건 안착 대기
            logger.info("Step 2: 물건 안착 대기 (2초)")
            time.sleep(2)
            
            # Step 3: 액추에이터 작동
            logger.info(f"Step 3: '{category}' 보관함으로 분류")
            
            # Step 4: 액추에이터 복귀 대기
            logger.info("Step 4: 액추에이터 복귀 대기 (1초)")
            time.sleep(1)
            
            # Step 5: 컨베이어 벨트 비활성화
            logger.info("Step 5: 컨베이어 벨트 정지")
            ConveyorBelt.disable()
            
            logger.info("=" * 60)
            logger.info(f"물건 처리 완료 - '{category}' 보관함에 저장됨\n")
            
        except Exception as e:
            logger.error(f"물건 처리 중 오류: {e}")
            # 에러 발생 시 안전하게 정지
            ConveyorBelt.disable()
            raise
    
    @classmethod
    def emergency_stop(cls):
        """긴급 정지"""
        logger.warning("긴급 정지")
        ConveyorBelt.disable()
        logger.info("모든 하드웨어 정지 완료")
    
    @classmethod
    def run_full_test(cls):
        """전체 워크플로우 테스트"""
        logger.info("전체 워크플로우 테스트 시작")
        
        try:
            cls.initialize()
            
            # 테스트 시나리오 1: 지갑
            logger.info("\n" + "="*60)
            logger.info("테스트 케이스 1: 지갑 보관")
            logger.info("="*60)
            cls.process_item("wallet")
            time.sleep(2)
            
            # 테스트 시나리오 2: 휴대폰
            logger.info("\n" + "="*60)
            logger.info("테스트 케이스 2: 휴대폰 보관")
            logger.info("="*60)
            cls.process_item("phone")
            time.sleep(2)
            
            # 테스트 시나리오 3: 기타
            logger.info("\n" + "="*60)
            logger.info("테스트 케이스 3: 기타 물품 보관")
            logger.info("="*60)
            cls.process_item("etc")
            
            logger.info("\n" + "="*60)
            logger.info("전체 테스트 완료!")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"테스트 실패: {e}")
        finally:
            cls.cleanup()


# 독립 실행 시 테스트
if __name__ == "__main__":
    try:
        HardwareController.run_full_test()
    except KeyboardInterrupt:
        logger.info("사용자에 의해 중단됨")
        HardwareController.emergency_stop()
        HardwareController.cleanup()