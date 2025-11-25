"""
액추에이터 제어 모듈
실제 하드웨어 연결 전까지 Mock으로 동작
"""
import time
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

# 실제 액추에이터 사용 여부 (현재 테스트, 하드웨어 연결 후 True로 변경 필요)
USE_REAL_ACTUATOR = False

if USE_REAL_ACTUATOR:
    import RPi.GPIO as GPIO


class Actuator:
    """액추에이터 제어 클래스"""
    
    # 액추에이터별 GPIO 핀 (실제 배선에 맞게 수정 필요)
    ACTUATOR_1_PIN = 17  # 1번 보관함용 (예: 지갑)
    ACTUATOR_2_PIN = 27  # 2번 보관함용 (예: 휴대폰)
    ACTUATOR_3_PIN = 22  # 3번 보관함용 (예: 기타)
    
    # 액추에이터 작동 시간 (초)
    PUSH_DURATION = 1.0    # 밀어내는 시간
    RETURN_DURATION = 1.0  # 복귀 시간
    
    _initialized = False
    
    # 카테고리 → 액추에이터 매핑
    CATEGORY_MAP = {
        "wallet": ACTUATOR_1_PIN,
        "phone": ACTUATOR_2_PIN,
        "card": ACTUATOR_1_PIN,      # 카드도 지갑과 같은 통
        "key": ACTUATOR_2_PIN,        # 열쇠
        "etc": ACTUATOR_3_PIN,        # 기타
        "default": ACTUATOR_1_PIN     # 인식 실패 시 기본
    }
    
    @classmethod
    def initialize(cls):
        """GPIO 초기화 (실제 하드웨어 사용 시)"""
        if cls._initialized:
            logger.warning("액추에이터가 이미 초기화되어 있습니다.")
            return
        
        if USE_REAL_ACTUATOR:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(cls.ACTUATOR_1_PIN, GPIO.OUT)
                GPIO.setup(cls.ACTUATOR_2_PIN, GPIO.OUT)
                GPIO.setup(cls.ACTUATOR_3_PIN, GPIO.OUT)
                
                # 초기 상태: 모두 OFF
                GPIO.output(cls.ACTUATOR_1_PIN, GPIO.LOW)
                GPIO.output(cls.ACTUATOR_2_PIN, GPIO.LOW)
                GPIO.output(cls.ACTUATOR_3_PIN, GPIO.LOW)
                
                cls._initialized = True
                logger.info("액추에이터 GPIO 초기화 완료 (실제 하드웨어)")
                
            except Exception as e:
                logger.error(f"액추에이터 GPIO 초기화 실패: {e}")
                raise
        else:
            cls._initialized = True
            logger.info("테스트: 액추에이터 초기화 완료")
    
    @classmethod
    def cleanup(cls):
        """GPIO 정리"""
        if cls._initialized and USE_REAL_ACTUATOR:
            # GPIO cleanup은 ConveyorBelt에서 한 번만 호출
            pass
        cls._initialized = False
        logger.info("액추에이터 cleanup 완료")
    
    @classmethod
    def push_to_bin(cls, category: str):
        """
        카테고리에 따라 해당 보관함으로 물건을 밀어넣기
        
        Args:
            category: AI가 분류한 카테고리 ("wallet", "phone", etc.)
        """
        if not cls._initialized:
            raise RuntimeError("액추에이터가 초기화되지 않았습니다. initialize()를 먼저 호출하세요.")
        
        # 카테고리에 맞는 액추에이터 핀 선택
        pin = cls.CATEGORY_MAP.get(category.lower(), cls.CATEGORY_MAP["default"])
        
        logger.info(f"'{category}' → {cls._get_bin_name(pin)} 보관함으로 밀어넣기")
        
        if USE_REAL_ACTUATOR:
            cls._activate_real_actuator(pin)
        else:
            cls._activate_mock_actuator(pin)
    
    @classmethod
    def _activate_real_actuator(cls, pin):
        """실제 액추에이터 작동"""
        try:
            # 액추에이터 확장 (물건 밀어내기)
            logger.info(f"   → GPIO {pin} HIGH (확장)")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(cls.PUSH_DURATION)
            
            # 액추에이터 복귀
            logger.info(f"   → GPIO {pin} LOW (복귀)")
            GPIO.output(pin, GPIO.LOW)
            time.sleep(cls.RETURN_DURATION)
            
            logger.info(f"액추에이터 작동 완료 (GPIO {pin})")
            
        except Exception as e:
            logger.error(f"액추에이터 작동 실패: {e}")
            raise
    
    @classmethod
    def _activate_mock_actuator(cls, pin):
        """Mock 액추에이터 (시뮬레이션)"""
        logger.info(f"[MOCK] GPIO {pin} HIGH (확장) - {cls.PUSH_DURATION}초 대기")
        time.sleep(cls.PUSH_DURATION)
        
        logger.info(f"[MOCK] GPIO {pin} LOW (복귀) - {cls.RETURN_DURATION}초 대기")
        time.sleep(cls.RETURN_DURATION)
        
        logger.info(f"[MOCK] 액추에이터 작동 완료 (GPIO {pin})")
    
    @classmethod
    def _get_bin_name(cls, pin):
        """핀 번호로 보관함 이름 반환 (로깅용)"""
        if pin == cls.ACTUATOR_1_PIN:
            return "1번"
        elif pin == cls.ACTUATOR_2_PIN:
            return "2번"
        elif pin == cls.ACTUATOR_3_PIN:
            return "3번"
        else:
            return "알 수 없음"
    
    @classmethod
    def run_test(cls):
        """테스트 모드 실행"""
        logger.info("액추에이터 테스트 시작")
        
        try:
            cls.initialize()
            
            logger.info("지갑 → 1번 보관함")
            cls.push_to_bin("wallet")
            time.sleep(0.5)
            
            logger.info("휴대폰 → 2번 보관함")
            cls.push_to_bin("phone")
            time.sleep(0.5)
            
            logger.info("기타 → 3번 보관함")
            cls.push_to_bin("etc")
            
            logger.info("테스트 완료")
            
        except Exception as e:
            logger.error(f"테스트 실패: {e}")
        finally:
            cls.cleanup()


# 독립 실행 시 테스트
if __name__ == "__main__":
    Actuator.run_test()