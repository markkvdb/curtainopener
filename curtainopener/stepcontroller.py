from time import sleep
import RPi.GPIO as GPIO


def motor_controller(to_open):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)

    p = GPIO.PWM(17, 5)
    p.start(0.1)

    try:
        sleep(100)
    except KeyboardInterrupt:
        pass

    p.stop()
    GPIO.cleanup()


