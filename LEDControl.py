import time


class LEDControl:
    
    PATTERN_MAX = 3
    DIM_MAX = 9
    SPEED_MAX = 2
    COLOR_MAX = 6

    LED_MAX = 255
    
    RED = 0
    GRN = 1
    BLU = 2

    def __init__(self):
        self.pattern = 0
        self.speed = 0
        self.color = 0
        self.dim = 5
        self.led = [0, 0, 0]
        self.switch_flag = 0

    def fadeup(self):
        for i in range(len(self.led)):
            self.led[i] += 1
            if self.led[i] > LEDControl.LED_MAX:
                self.led[i] = 0
        time.sleep(0.01)

    ########### CONTROL FUNCTIONS ###########
    def changeval(self, x, _max, _dir):
        if _dir == 1:
            return x+1 if x < _max else 0
        else:
            return x-1 if x > 0 else _max

    def changepattern(self, _dir):
        self.pattern = self.changeval(self.pattern, LEDControl.PATTERN_MAX, _dir)
    
    def changespeed(self, _dir):
        self.speed = self.changeval(self.speed, LEDControl.SPEED_MAX, _dir)
    
    def changedim(self, _dir):
        self.dim = self.changeval(self.dim, LEDControl.DIM_MAX, _dir)
                
    def changecolor(self, _dir):
        self.color = self.changeval(self.color, LEDControl.COLOR_MAX, _dir)

    ########### HELPER FUNCTIONS ###########
    # Function that converts 0-100 to 0-65536 for use from PWM
    def pwmconvert(self, x):
        return int(x * 65536 * self.dim / (LEDControl.LED_MAX*40))
