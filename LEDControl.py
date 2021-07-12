import time


class LEDControl:
    
    PATTERN_MAX = 3
    DIM_MAX = 9
    SPEED_MAX = 2

    LED_MAX = 255

    COLOR_VALS = [
        [1, 1, 1],      # white
        [1, 0, 0],      # red
        [1, 0.5, 0],    # orange
        [1, 1, 0],      # yellow
        [0.5, 1, 0],    # lime
        [0, 1, 0],      # green
        [0, 1, 0.5],    # jade
        [0, 1, 1],      # teal
        [0, 0.5, 1],    # azure
        [0, 0, 1],      # blue
        [0.5, 0, 1],    # violet
        [1, 0, 1],      # purple
        [1, 0, 0.5],    # pink
    ]

    RED = 0
    GRN = 1
    BLU = 2

    def __init__(self):
        self.pattern = 0
        self.speed = 0
        self.color = 0
        self.dim = 5
        self.led = [0, 0, 0]
        self.ledout = (0, 0, 0)
        self.dir = [0, 0, 0]
        self.speedint = []
        self.colorvals = []
        self.switch_flag = False
        self.changeclr_flag = False
        self.COLOR_MAX = 0

    ############################# RUN SCRIPT ##########################
    def run(self):
        if self.pattern == 0: self.off()
        elif self.pattern == 1: self.fadeup()
        elif self.pattern == 2: self.off()
        elif self.pattern == 3: self.off()

    ############################# LED CONTROL #########################
    def off(self):
        if self.switch_flag == True:
            self.led = [0, 0, 0]
            self.ledout = (0, 0, 0)
            self.switch_flag = False

    def fadeup(self):
        #Initial values
        if self.switch_flag == True:
            self.led = [0, 0, 0]
            self.dir = [1, 1, 1]
            self.color = 0
            self.speedint = [0.04, 0.02, 0.01]
            self.colorvals = LEDControl.COLOR_VALS
            self.COLOR_MAX = len(self.colorvals)-1
            self.switch_flag = False
        #If color is changed
        if self.changeclr_flag == True:
            self.led = [0, 0, 0]
            self.changeclr_flag = False
        #Thread that runs
        for i in range(len(self.led)):
            self.led[i] = 0 if self.led[i] > LEDControl.LED_MAX else self.led[i] + 1
        self.ledout = tuple(int(x * y * self.dim / self.DIM_MAX) for x, y in zip(self.led, self.colorvals[self.color]))
        time.sleep(self.speedint[self.speed])

    ########### CONTROL FUNCTIONS ###########
    def changeval(self, x, _max, _dir):
        if _dir == 1:
            return x+1 if x < _max else 0
        else:
            return x-1 if x > 0 else _max

    def changepattern(self, _dir):
        self.pattern = self.changeval(self.pattern, LEDControl.PATTERN_MAX, _dir)
        self.switch_flag = True
    
    def changespeed(self, _dir):
        self.speed = self.changeval(self.speed, LEDControl.SPEED_MAX, _dir)
    
    def changedim(self, _dir):
        self.dim = self.changeval(self.dim, LEDControl.DIM_MAX, _dir)
                
    def changecolor(self, _dir):
        self.color = self.changeval(self.color, self.COLOR_MAX, _dir)
        self.changeclr_flag = True

    ########### HELPER FUNCTIONS ###########
    # Function that converts 0-100 to 0-65536 for use from PWM
    def pwmconvert(self, x):
        return int(x * 65536 * self.dim / (LEDControl.LED_MAX*40))
