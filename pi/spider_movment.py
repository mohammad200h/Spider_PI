from minikame import MiniKame
from Servo import Servo
import time 
minikame = MiniKame(servo_pins = [i for i in range(1,9)])

minikame.walk(steps =1)







# lower limit 1500 us 
#upper limit 12000 us
# servo = Servo()
# servo.attach(3)
# servo.writeMicroseconds(1500)
# time.sleep(1)
# servo.writeMicroseconds(12000)
# time.sleep(1)
