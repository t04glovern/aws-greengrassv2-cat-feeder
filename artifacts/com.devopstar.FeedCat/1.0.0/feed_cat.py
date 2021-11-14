import sys
import time
import traceback
import logging

import RPi.GPIO as IO

# GPIO pins
GPIO_SERVO_PIN = 18

# Logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class CatFeeder():

    def __init__(self):
        IO.setmode(IO.BCM)
        IO.setup(GPIO_SERVO_PIN,IO.OUT)
        self.SERVO = IO.PWM(GPIO_SERVO_PIN,100)
        time.sleep(0.1)
        self._reset_feeder()

    def _reset_feeder(self):
        self._open_feeder(open_feeder=False)

    def _open_feeder(self, open_feeder):
        self.SERVO.start(0)
        time.sleep(0.1)
        if open_feeder:
            # PWM Signal to open the servo
            self.SERVO.ChangeDutyCycle(30)
        else:
            # PWM Signal to close the servo
            self.SERVO.ChangeDutyCycle(15)
        time.sleep(0.5)
    
    def _clear(self):
        self.SERVO.stop()
        IO.cleanup()

if __name__ == '__main__':
    try:
        print(f"Hello, {sys.argv[1]}!")
        feeder = CatFeeder()
        feeder._open_feeder(open_feeder=True)
        time.sleep(1.5)
        feeder._reset_feeder()
        feeder._clear()
    except:
        log.error(traceback.format_exc())
