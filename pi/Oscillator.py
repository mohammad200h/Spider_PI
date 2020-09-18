
from util import millis

from math import sin
PI = 3.14159 
class Oscillator :
    def __init__(self):
        self._period =2000
        self._amplitude = 50
        self._phase = 0
        self._offset = 0
        self._output =0
        self._stop = True
        self._ref_time = millis()
        self._delta_time = 0        

    def refresh(self):
        if(not self._stop):
            self._delta_time = (millis()-self._ref_time)%self._period
            self._output = float(self._amplitude)*sin(self.time_to_radians(self._delta_time))
            +self.degrees_to_radians(self._phase)+self._offset

        return self._output
    def reset(self):
        self._ref_time = millis()
    def start(self,ref_time = None):
        if ref_time ==None:
            self.reset()
            self._stop = False
        else:
            self._ref_time = ref_time
            self._stop = false
    def stop(self):
        self._stop = True
    def time_to_radians(self,time):
         return time*2*PI/self._period
    def degrees_to_radians(self,degrees):
        return degrees*2*PI/360
    def degrees_to_time(self,degrees):
        return degrees*self._period/360
    def setPeriod(self,period):
        self._period = period
    def setAmplitude(self,amplitude):
        self._amplitude = amplitude
    def setPhase(self,phase):
        self._phase = phase
    def setOffset(self,offset):
        self._offset = offset
    def setTime(self,ref):
        self._ref_time = ref
    def getOutput(self):
        return self._output
    def getPhaseProgress(self):
        return (float(self._delta_time)/self._period) * 360
    def getTime(self):
        return self._ref_time

