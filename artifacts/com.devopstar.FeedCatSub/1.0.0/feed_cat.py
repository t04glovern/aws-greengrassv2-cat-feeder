import concurrent.futures
import sys
import time
import traceback
import logging

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    SubscribeToTopicRequest,
    SubscriptionResponseMessage,
    UnauthorizedError
)

import RPi.GPIO as IO

# Logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# GPIO pins
GPIO_SERVO_PIN = 18

topic = "devopstar/cat-feeder/feed"
TIMEOUT = 10


class StreamHandler(client.SubscribeToTopicStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: SubscriptionResponseMessage) -> None:
        try:
            message = str(event.binary_message.message, "utf-8")
            log.info("Received message: %s", message)

            # Feed cat
            try:
                feeder = CatFeeder()
                feeder._open_feeder(open_feeder=True)
                time.sleep(1.5)
                feeder._reset_feeder()
                feeder._clear()
            except:
                log.error(traceback.format_exc())
        except:
            log.error(traceback.format_exc())

    def on_stream_error(self, error: Exception) -> bool:
        log.error("Received a stream error.: %s", error)
        log.error(traceback.format_exc())
        return False  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        log.info("Subscribe to topic stream closed.")


class CatFeeder():

    def __init__(self):
        IO.setmode(IO.BCM)
        IO.setup(GPIO_SERVO_PIN,IO.OUT)
        self.SERVO = IO.PWM(GPIO_SERVO_PIN,50)
        time.sleep(0.1)
        self._reset_feeder()

    def _reset_feeder(self):
        self._open_feeder(open_feeder=False)

    def _open_feeder(self, open_feeder):
        self.SERVO.start(0)
        time.sleep(0.1)
        if open_feeder:
            # PWM Signal to open the servo
            self.SERVO.ChangeDutyCycle(7.0)
        else:
            # PWM Signal to close the servo
            self.SERVO.ChangeDutyCycle(2.5)
        time.sleep(0.5)
    
    def _clear(self):
        self.SERVO.stop()
        IO.cleanup()

try:
    ipc_client = awsiot.greengrasscoreipc.connect()

    request = SubscribeToTopicRequest()
    request.topic = topic
    handler = StreamHandler()
    operation = ipc_client.new_subscribe_to_topic(handler)
    future = operation.activate(request)
    
    try:
        future.result(TIMEOUT)
        log.info('Successfully subscribed to topic: ' + topic)
    except concurrent.futures.TimeoutError as e:
        log.error('Timeout occurred while subscribing to topic: ' + topic)
        raise e
    except UnauthorizedError as e:
        log.error('Unauthorized error while subscribing to topic: ' + topic)
        raise e
    except Exception as e:
        log.error('Exception while subscribing to topic: ' + topic)
        raise e

    # Keep the main thread alive, or the process will exit.
    try:
        while True:
            time.sleep(10)
    except InterruptedError:
        log.error('Subscribe interrupted.')
except Exception:
    log.error('Exception occurred when using IPC.')
    log.error(traceback.format_exc())
    exit(1)
