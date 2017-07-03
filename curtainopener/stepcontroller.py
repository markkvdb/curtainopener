from time import sleep
import RPi.GPIO as GPIO

from .alarm import Alarm


def motor_controller(alarm):
    number_of_steps = 10
    duration_motor = 50 * (100 / alarm.speed)

    total_time_per_step = int(alarm.seconds_to_last / number_of_steps)
    motor_time_per_step = int(duration_motor / number_of_steps)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

    GPIO.output(4, not alarm.open)

    try:
        for time in range(0, number_of_steps):
            p = GPIO.PWM(17, alarm.speed)
            GPIO.output(22, True)
            p.start(0.1)
            sleep(motor_time_per_step)
            p.stop()
            GPIO.output(22, False)
            sleep(total_time_per_step - motor_time_per_step)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
