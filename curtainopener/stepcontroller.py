from time import sleep
import RPi.GPIO as GPIO

from .alarm import Alarm


def motor_controller(alarm):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)

    p = GPIO.PWM(17, 5)
    p.start(0.1)

    try:
        sleep(100)
    except KeyboardInterrupt:
        print('Motor is interrupted.')
        pass

    p.stop()
    GPIO.cleanup()
