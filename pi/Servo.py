
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
class Servo:
    def __init__(self):
        self.pin = None
        self.servo_start = True
        self.servo = None
    def attach(self,pin):
        self.pin = pin
        GPIO.setup(pin,GPIO.OUT)
        self.servo = GPIO.PWM(pin, 50)
        # print("\n")
        # print("self.servo:: ",self.servo)
        # print("\n")
    def writeMicroseconds(self,us):
     
        dutyCycle = us/1000 #some math converting us to appropraite dutycycle for pi
        print("writeMicroseconds::us:: ",us)
        print("writeMicroseconds::dutyCycle:: ",dutyCycle)
        if self.servo_start:
            self.servo.start(dutyCycle)
        else:
            self.servo.ChangeDutyCycle(dutyCycle)