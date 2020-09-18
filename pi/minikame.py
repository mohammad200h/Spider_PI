import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip3", "install", package])

from Oscillator import Oscillator

from Servo import Servo
try:
    from adafruit_servokit import ServoKit
except:
    install("adafruit-circuitpython-pca9685")
    install("adafruit-circuitpython-servokit")
from util import millis, delay

#us
MAX_PULSE_WIDTH  = 12000 
MIN_PULSE_WIDTH  = 1500



class MiniKame :
    def __init__(self,servo_pins=None,trim =8*[0]):
        self._oscillator = [Oscillator() for os in range(0,8)]
        self._servo = [Servo() for os in range(0,8)]
        self._board_pins = 8*[0]
        self._trim = 8*[0]
        self._reverse = 8*[False]
        self._init_time = None
        self._final_time = None
        self._partial_time = None
        self._increment = 8*[0]
        self._servo_position = 8*[0]

        self._init_servo_pins(servo_pins)
        self._init_trim(trim)
        self._init_per_servo()

    def angToUsec(self,value):
        return value/120 * (MAX_PULSE_WIDTH-MIN_PULSE_WIDTH) + MIN_PULSE_WIDTH
    def _execute(self,steps,period,amplitude, offset,phase):
        for i in range(8):
            self._oscillator[i].setPeriod(period[i])
            self._oscillator[i].setAmplitude(amplitude[i])
            self._oscillator[i].setPhase(phase[i])
            self._oscillator[i].setOffset(offset[i])


        global_time = millis()

        for i in range(8): self._oscillator[i].setTime(global_time)

        self._final_time = millis() + period[0]*steps
        while (millis() < self._final_time):
            for i in range(8):
                self.setServo(i, self._oscillator[i].refresh())
            
            yield
        
    
    def run(self,steps,T =600):
        x_amp = 15
        z_amp = 15
        ap = 15
        hi = 15
        front_x = 6
        period = [T, T, T, T, T, T, T, T]
        amplitude = [x_amp,x_amp,z_amp,z_amp,x_amp,x_amp,z_amp,z_amp]
        offset = [    90+ap-front_x,
                            90-ap+front_x,
                            90-hi,
                            90+hi,
                            90-ap-front_x,
                            90+ap+front_x,
                            90+hi,
                            90-hi
                        ]
        phase = [0,0,90,90,180,180,90,90] 
        self._execute(steps,period,amplitude,offset,phase)  
    def walk(self,steps,T=5000):
        x_amp = 15
        z_amp = 20
        ap = 20
        hi = 10
        front_x = 12
        period = [T, T, T/2, T/2, T, T, T/2, T/2]
        amplitude = [x_amp,x_amp,z_amp,z_amp,x_amp,x_amp,z_amp,z_amp]
        offset = [   90+ap-front_x,
                                    90-ap+front_x,
                                    90-hi,
                                    90+hi,
                                    90-ap-front_x,
                                    90+ap+front_x,
                                    90+hi,
                                    90-hi
                        ]
        phase = [90, 90, 270, 90, 270, 270, 90, 270]

        for i in range(8):
            self._oscillator[i].reset()
            self._oscillator[i].setPeriod(period[i])
            self._oscillator[i].setAmplitude(amplitude[i])
            self._oscillator[i].setPhase(phase[i])
            self._oscillator[i].setOffset(offset[i])


        self._final_time = millis() + period[0]*steps
        self._init_time = millis()
        side = None
        while (millis() < self._final_time):
            side = int((millis()-self._init_time) / (period[0]/2)) % 2
            self.setServo(0, self._oscillator[0].refresh())
            self.setServo(1, self._oscillator[1].refresh())
            self.setServo(4, self._oscillator[4].refresh())
            self.setServo(5, self._oscillator[5].refresh())

            if (side == 0):
                self.setServo(3, self._oscillator[3].refresh())
                self.setServo(6, self._oscillator[6].refresh())

            else:
                oss = self._oscillator[2].refresh()
                self.setServo(2,oss )
                print("oss::",oss)
                self.setServo(7, self._oscillator[7].refresh())

            delay(1)
    def omniWalk(self,steps,T,side,turn_factor):
        x_amp = 15
        z_amp = 15
        ap = 15
        hi = 23
        front_x = 6 * (1-pow(turn_factor, 2))
        period = [T, T, T, T, T, T, T, T]
        amplitude = [x_amp,x_amp,z_amp,z_amp,x_amp,x_amp,z_amp,z_amp]
        offset = [ 90+ap-front_x,
                   90-ap+front_x,
                   90-hi,
                   90+hi,
                   90-ap-front_x,
                   90+ap+front_x,
                   90+hi,
                   90-hi
                ]

        phase = 8*[0]
        if (side):
            phase1 =  [0,   0,   90,  90,  180, 180, 90,  90]
            phase2R = [0,   180, 90,  90,  180, 0,   90,  90]
            for i in range(8):
                phase[i] = phase1[i]*(1-turn_factor) + phase2R[i]*turn_factor

        else:
            phase1 =  [0,   0,   90,  90,  180, 180, 90,  90]
            phase2L = [180, 0,   90,  90,  0,   180, 90,  90]
            for i in range(8):
                phase[i] = phase1[i]*(1-turn_factor) + phase2L[i]*turn_factor + oscillator[i].getPhaseProgress()

        self._execute(steps,period,amplitude,offset,phase)  
    def turnL(self,steps,T =600):
        x_amp = 15
        z_amp = 15
        ap = 15
        hi = 23
        period = [T, T, T, T, T, T, T, T]
        amplitude = [x_amp,x_amp,z_amp,z_amp,x_amp,x_amp,z_amp,z_amp]
        offset = [90+ap,90-ap,90-hi,90+hi,90-ap,90+ap,90+hi,90-hi]
        phase = [180,0,90,90,0,180,90,90]
        self._execute(steps,period,amplitude,offset,phase)
    def turnR(self,steps,T =600):
        x_amp = 15
        z_amp = 15
        ap = 15
        hi = 23
        period = [T, T, T, T, T, T, T, T]
        amplitude = [x_amp,x_amp,z_amp,z_amp,x_amp,x_amp,z_amp,z_amp]
        offset = [90+ap,90-ap,90-hi,90+hi,90-ap,90+ap,90+hi,90-hi]
        phase = [0,180,90,90,180,0,90,90]
        self._execute(steps,period,amplitude,offset,phase)
    def moonwalkL(self,steps,T=5000):
        z_amp = 45
        period = [T, T, T, T, T, T, T, T]
        amplitude = [0,0,z_amp,z_amp,0,0,z_amp,z_amp]
        offset = [90, 90, 90, 90, 90, 90, 90, 90]
        phase = [0,0,0,120,0,0,180,290]
        self._execute(steps,period,amplitude,offset,phase)
    def dance(self,steps,T =600):
        x_amp = 0
        z_amp = 40
        ap = 30
        hi = 20
        period = [T, T, T, T, T, T, T, T]
        amplitude = [x_amp,x_amp,z_amp,z_amp,x_amp,x_amp,z_amp,z_amp]
        offset = [90+ap,90-ap,90-hi,90+hi,90-ap,90+ap,90+hi,90-hi]
        phase = [0,0,0,270,0,0,90,180]
        self._execute(steps,period,amplitude,offset,phase)
    def upDown(self,steps, T=5000):
        x_amp = 0
        z_amp = 35
        ap = 20
        hi = 25
        front_x = 0
        period = [T, T, T, T, T, T, T, T]
        amplitude = [x_amp,x_amp,z_amp,z_amp,x_amp,x_amp,z_amp,z_amp]
        offset = [    90+ap-front_x,
                            90-ap+front_x,
                            90-hi,
                            90+hi,
                            90-ap-front_x,
                            90+ap+front_x,
                            90+hi,
                            90-hi
                        ]
        phase = [0,0,90,270,180,180,270,90]
        self._execute(steps,period,amplitude,offset,phase)  
    def frontBack(self,steps,T =600):
        x_amp = 30
        z_amp = 25
        ap = 20
        hi = 30
        period = [T, T, T, T, T, T, T, T]
        amplitude = [x_amp,x_amp,z_amp,z_amp,x_amp,x_amp,z_amp,z_amp]
        offset = [90+ap,90-ap,90-hi,90+hi,90-ap,90+ap,90+hi,90-hi]
        phase = [0,180,270,90,0,180,90,270]
        self._execute(steps,period,amplitude,offset,phase)
    def pushUp(self,steps,T=600):
        z_amp = 40
        x_amp = 65
        hi = 30
        period = [T, T, T, T, T, T, T, T]
        amplitude = [0,0,z_amp,z_amp,0,0,0,0]
        offset = [90,90,90-hi,90+hi,90-x_amp,90+x_amp,90+hi,90-hi]
        phase = [0,0,0,180,0,0,0,180]
        self._execute(steps,period,amplitude,offset,phase)  
    def hello(self):
        sentado=[90+15,90-15,90-65,90+65,90+20,90-20,90+10,90-10]
        moveServos(150, sentado)
        delay(200)

        z_amp = 40
        x_amp = 60
        T=350
        period = [T, T, T, T, T, T, T, T]
        amplitude = [0,50,0,50,0,0,0,0]
        offset = [90+15,40,90-65,90,90+20,90-20,90+10,90-10]
        phase = [0,0,0,90,0,0,0,0]
        self._execute(steps,period,amplitude,offset,phase)
    def jump(self):
        sentado=[90+15,90-15,90-65,90+65,90+20,90-20,90+10,90-10]
        ap = 20.0
        hi = 35.0
        salto = [90+ap,90-ap,90-hi,90+hi,90-ap*3,90+ap*3,90+hi,90-hi]
        moveServos(150, sentado)
        delay(200)
        moveServos(0, salto)
        delay(100)
        home() 
    def home(self):
        ap = 20
        hi = 35
        position = [90+ap,90-ap,90-hi,90+hi,90-ap,90+ap,90+hi,90-hi]
        for i in range(8):
            self.setServo(i, position[i])

    def zero(self):
        for i in range(8):
            self.setServo(i, 90)

    def setServo(self,id,target):
        if (not self._reverse[id]):
            self._servo[id].writeMicroseconds(self.angToUsec(target+self._trim[id]))
        else:
            self._servo[id].writeMicroseconds(self.angToUsec(180-(target+self._trim[id])))
        self._servo_position[id] = target
    def reverseServo(id):
        if (self._reverse[id]):
            self._reverse[id] = False
        else:
            self._reverse[id] = True
    def getServo(id):
        return _servo_position[id]
    def moveServos(time, target):#target is an array
        if (time>10):
            for i in range(8):	self._increment[i] = (target[i] - self._servo_position[i]) / (time / 10.0)
            self._final_time =  millis() + time

            while (millis() < self._final_time):
                self._partial_time = millis() + 10
                for i in range(8): self.setServo(i, self._servo_position[i] + self._increment[i])
                while (millis() < self._partial_time): #pause
                    delay(1)

        else:
            for i in range(8): self.setServo(i, target[i])
        
        for i in range(8): self._servo_position[i] = target[i]
    #utility functions
    def _init_servo_pins(self,pins=None):
        if pins == None:
            print("please set the pins for servo")
        else:
            if len(pins)==len(self._board_pins):
                for i,pin in enumerate(pins):
                    self._board_pins[i]= pin
            else:
                print("the lengeht of the servo pins should be equal to 8")
    def _init_trim(self,trim):
        if len(trim) == len(self._trim):
            for i,tr in enumerate(trim):
                self._trim[i]= tr
        else:
            print("len of trim should be equal to servo numbers")
    def _init_per_servo(self):
        
        for i,pin in enumerate(self._board_pins):
            self._oscillator[i].start()
            self._servo[i].attach(pin)
        self.zero()




class MiniKame_PCA9685(MiniKame):
    def __init__(self,servo_pins=None,trim =8*[0]):
        super().__init__(servo_pins, trim)
        self.servo = ServoKit(channels=8).servo
    
    def setServo(id,target):
        if (not reverse[id]):
            self.servo[id].angle = target+self._trim[id]
        else:
            self.servo[id].angle = 120-(target+self._trim[id])
         
        self._servo_position[id] = target








"""
sudo pip3 install adafruit-circuitpython-pca9685
sudo pip3 install adafruit-circuitpython-servokit
"""