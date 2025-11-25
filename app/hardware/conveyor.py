"""
컨베이어 벨트 제어 모듈
TB6600 스테퍼 모터 드라이버 사용
"""
import RPi.GPIO as GPIO
import time
from app.utils.logger_config import setup_logger

logger = setup_logger(__name__)

class ConveyorBelt:
    """컨베이어 벨트 제어 클래스"""
    
    # GPIO 핀 설정
    PUL = 18  # Pulse
    DIR = 23  # Direction
    ENA = 24  # Enable
    
    # 기본 설정값
    DEFAULT_STEPS = 7000       # 기본 이동 스텝 수
    DEFAULT_SPEED = 0.0005     # 기본 속도 (딜레이)
    DIRECTION_FORWARD = 0      # 정방향
    DIRECTION_BACKWARD = 1     # 역방향
    
    _initialized = False       # GPIO 초기화 상태
    
    @classmethod
    def initialize(cls):
        """GPIO 초기화 (프로그램 시작 시 1회만 호출)"""
        if cls._initialized:
            logger.warning("컨베이어벨트가 이미 초기화되어 있습니다.")
            return
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(cls.PUL, GPIO.OUT)
            GPIO.setup(cls.DIR, GPIO.OUT)
            GPIO.setup(cls.ENA, GPIO.OUT)
            
            # 모터 비활성화 상태로 시작
            GPIO.output(cls.ENA, GPIO.HIGH)
            
            cls._initialized = True
            logger.info("컨베이어벨트 GPIO 초기화 완료")
            
        except Exception as e:
            logger.error(f"컨베이어벨트 GPIO 초기화 실패: {e}")
            raise
    
    @classmethod
    def cleanup(cls):
        """GPIO 정리 (프로그램 종료 시 호출)"""
        if cls._initialized:
            GPIO.cleanup()
            cls._initialized = False
            logger.info("GPIO cleanup 완료")
    
    @classmethod
    def enable(cls):
        """모터 활성화"""
        GPIO.output(cls.ENA, GPIO.LOW)
        logger.info("컨베이어 벨트 모터 활성화")
    
    @classmethod
    def disable(cls):
        """모터 비활성화"""
        GPIO.output(cls.ENA, GPIO.HIGH)
        logger.info("컨베이어 벨트 모터 비활성화")
    
    @classmethod
    def move_forward(cls, steps=None, speed=None):
        """
        정방향으로 이동
        
        Args:
            steps: 이동할 스텝 수 (None이면 DEFAULT_STEPS 사용)
            speed: 속도 (딜레이 시간, None이면 DEFAULT_SPEED 사용)
        """
        if not cls._initialized:
            raise RuntimeError("컨베이어벨트가 초기화되지 않았습니다. initialize()를 먼저 호출하세요.")
        
        steps = steps or cls.DEFAULT_STEPS
        speed = speed or cls.DEFAULT_SPEED
        
        logger.info(f"컨베이어 벨트 정방향 이동 시작 (steps={steps}, speed={speed})")
        for i in range(10):
          GPIO.output(cls.PUL, GPIO.HIGH)
          time.sleep(0.001)
          GPIO.output(cls.PUL, GPIO.LOW)
          time.sleep(0.001)
          logger.info(f"PULSE {i}")
        cls._step_motor(cls.DIRECTION_FORWARD, steps, speed)
        logger.info("정방향 이동 완료")
    
    @classmethod
    def _step_motor(cls, direction, steps, speed):
        """
        스테퍼 모터 구동 (내부 함수)
        
        Args:
            direction: 방향 (0=정방향, 1=역방향)
            steps: 스텝 수
            speed: 펄스 간 딜레이
        """
        GPIO.output(cls.DIR, direction)

        logger.info(f"[DEBUG] initialized={cls._initialized}")
        logger.info(f"[DEBUG] ENA pin={GPIO.input(cls.ENA)}")
        
        for i in range(steps):
            GPIO.output(cls.PUL, GPIO.HIGH)
            time.sleep(speed)
            GPIO.output(cls.PUL, GPIO.LOW)
            time.sleep(speed)

            if i < 10:
              logger.info(f"[DEBUG] pulse {i}")
    
    @classmethod
    def run_test(cls):
        """테스트 모드 실행"""
        logger.info("컨베이어 벨트 테스트 시작")
        
        try:
            cls.initialize()
            cls.enable()
            
            logger.info("정방향 테스트")
            cls.move_forward(steps=5000)
            time.sleep(1)
            
            # logger.info("고속 테스트")
            # cls.move_forward(steps=2000, speed=0.0003)
            
            cls.disable()
            logger.info("테스트 완료")
            
        except Exception as e:
            logger.error(f"테스트 실패: {e}")
        finally:
            cls.cleanup()


# 독립 실행 시 테스트
if __name__ == "__main__":
    ConveyorBelt.run_test()