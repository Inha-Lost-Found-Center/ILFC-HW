import RPi.GPIO as GPIO
import time

# === Pin Mapping ===
PUL = 18   # Pulse
DIR = 23   # Direction
ENA = 24   # Enable

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# === 모터 활성화 ===
GPIO.output(ENA, GPIO.LOW)   # ENA LOW = Enable

def step_motor(direction, steps, speed=0.0005):
    """
    direction: 0 = 정방향, 1 = 역방향
    steps: 스텝 수
    speed: 펄스 간 딜레이 (작을수록 빠름)
    """
    GPIO.output(DIR, direction)

    for _ in range(steps):
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(speed)

try:
    print("모터 테스트 시작")

    step_motor(0, 7000, 0.0005)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    print("GPIO Clean up 완료")