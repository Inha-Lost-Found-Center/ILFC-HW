import RPi.GPIO as GPIO
import time

# === Pin Mapping (너가 배선한 그대로) ===
PUL = 18   # Pulse
DIR = 23   # Direction
ENA = 24   # Enable

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# === 모터 활성화 ===
GPIO.output(ENA, GPIO.LOW)   # ENA LOW = Enable (TB6600 보드에 따라 HIGH일 수도 있음)
# 반대로 동작하면 HIGH로 바꿔줘!

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

    print("정방향으로 200스텝")
    step_motor(0, 7000, 0.0005)

    #time.sleep(1)

    print("역방향으로 200스텝")
    #step_motor(1, 1200, 0.001)

    #ime.sleep(1)

    print("저속 회전 (속도 느리게)")
    #step_motor(0, 200, 0.005)

    #time.sleep(1)

    print("고속 회전 (속도 빠르게)")
    #step_motor(0, 200, 0.0005)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    print("GPIO Clean up 완료")