from time import sleep
import RPi.GPIO as GPIO


def motor_controller(to_open):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)

    output_17 = True

    try:
        while True:
            GPIO.output(17, output_17)
            output_17 = not output_17
            sleep(0.0015)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()


