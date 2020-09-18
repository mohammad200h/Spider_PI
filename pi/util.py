import time
def millis():
    millis = int(round(time.time() * 1000000))
    return millis

def delay(t):
    # ms =1/1000 
    # time.sleep(ms*t)
    time.sleep(t)