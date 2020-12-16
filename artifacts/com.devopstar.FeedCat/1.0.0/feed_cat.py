import RPi.GPIO as IO
import sys
import time

IO.setmode(IO.BCM)

# GPIO pins
GPIO_SERVO_PIN = 18

IO.setup(GPIO_SERVO_PIN,IO.OUT)
SERVO = IO.PWM(GPIO_SERVO_PIN,100)

class CatFeeder():

    def __init__(self):
        self._reset_feeder()

    def _reset_feeder(self):
        self._open_feeder(open_feeder=False)

    def _open_feeder(self, open_feeder):
        SERVO.start(0)
        if open_feeder:
            # PWM Signal to open the servo
            SERVO.ChangeDutyCycle(30)
        else:
            # PWM Signal to close the servo
            SERVO.ChangeDutyCycle(15)

if __name__ == '__main__':
    try:
        print(f"Hello, {sys.argv[1]}!")
        feeder = CatFeeder()
        time.sleep(1)
        feeder._open_feeder(open_feeder=True)
        time.sleep(3)
        feeder._reset_feeder()
    finally:
        IO.cleanup()
