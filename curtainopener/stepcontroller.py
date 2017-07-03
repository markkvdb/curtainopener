import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)    # Step
GPIO.setup(4, GPIO.OUT)     # Direction True = CCW, Fale = CW
GPIO.setup(22, GPIO.OUT)    # Enable controller

bool openclose = True

GPIO.output(22, True)       # Enable the stepper controller
GPIO.output(4, openclose)   # Set Direction
p = GPIO.PWM(17, 520)       # Setup PWM
p.start(0.1)                # Make steps

# Stop after some time

output_22 = False   # Turn off stepper contoller
p.stop()
GPIO.cleanup()
