import time
import threading
import os
import tkinter
from functools import partial
from LEDControl import LEDControl

led = LEDControl()
mutex = threading.Lock()


def convert_2_hex(color_list):
    rtn_string = str("#")
    for i in color_list:
        hex_list = [int(i / 16), int(i % 16)]
        for j in hex_list:
            if 0 <= j <= 9: rtn_string += str(j)
            elif j == 10: rtn_string += str("a")
            elif j == 11: rtn_string += str("b")
            elif j == 12: rtn_string += str("c")
            elif j == 13: rtn_string += str("d")
            elif j == 14: rtn_string += str("e")
            elif j == 15: rtn_string += str("f")
    return rtn_string if len(rtn_string)==7 else "#000000"


def disp_leds():
    os.system('clear')
    while True:
        mutex.acquire()
        try:
            print("LED RED: ", led.ledout[0], "\nLED GREEN: ", led.ledout[1], "\nLED BLUE: ", led.ledout[2])
            print("Hex value: " + convert_2_hex(led.ledout))
            print("\nPattern: ", led.pattern)
            print("Dim: ", led.dim)
            print("Color: ", led.color)
            print("Speed: ", led.speed)
        finally:
            mutex.release()
        time.sleep(0.001)
        # os.system('clear')


t1 = threading.Thread(target=disp_leds)
# t1.start()

def tkinter_script():
    pattern_str = "Pattern: " + str(led.pattern)
    speed_str = "Speed: " + str(led.speed)
    color_str = "Color: " + str(led.color)
    dim_str = "Dim: " + str(led.dim)

    window = tkinter.Tk()

    def pattern_label_change(_dir):
        led.changepattern(_dir)
        pattern_str = "Pattern: " + str(led.pattern)
        pattern_label.config(text=pattern_str)

    def speed_label_change(_dir):
        led.changespeed(_dir)
        speed_str = "Speed: " + str(led.speed)
        speed_label.config(text=speed_str)

    def color_label_change(_dir):
        led.changecolor(_dir)
        color_str = "Color: " + str(led.color)
        color_label.config(text=color_str)

    def dim_label_change(_dir):
        led.changedim(_dir)
        dim_str = "Dim: " + str(led.dim)
        dim_label.config(text=dim_str)

    pattern_frame = tkinter.Frame(window)
    pattern_frame.pack(side=tkinter.LEFT)
    pattern_label = tkinter.Label(pattern_frame, text=pattern_str)
    pattern_up_but = tkinter.Button(pattern_frame, text="↑", command=partial(pattern_label_change, 1))
    pattern_down_but = tkinter.Button(pattern_frame, text="↓", command=partial(pattern_label_change, 0))
    pattern_label.pack(side=tkinter.LEFT)
    pattern_up_but.pack()
    pattern_down_but.pack()

    color_frame = tkinter.Frame(window)
    color_frame.pack(side=tkinter.LEFT)
    color_label = tkinter.Label(color_frame, text=color_str)
    color_label.pack(side=tkinter.LEFT)
    color_up_but = tkinter.Button(color_frame, text="↑", command=partial(color_label_change, 1))
    color_up_but.pack()
    color_down_but = tkinter.Button(color_frame, text="↓", command=partial(color_label_change, 0))
    color_down_but.pack()

    dim_frame = tkinter.Frame(window)
    dim_frame.pack(side=tkinter.LEFT)
    dim_label = tkinter.Label(dim_frame, text=dim_str)
    dim_label.pack(side=tkinter.LEFT)
    dim_up_but = tkinter.Button(dim_frame, text="↑", command=partial(dim_label_change, 1))
    dim_up_but.pack()
    dim_down_but = tkinter.Button(dim_frame, text="↓", command=partial(dim_label_change, 0))
    dim_down_but.pack()

    speed_frame = tkinter.Frame(window)
    speed_frame.pack(side=tkinter.LEFT)
    speed_label = tkinter.Label(speed_frame, text=speed_str)
    speed_label.pack(side=tkinter.LEFT)
    speed_up_but = tkinter.Button(speed_frame, text="↑", command=partial(speed_label_change, 1))
    speed_up_but.pack()
    speed_down_but = tkinter.Button(speed_frame, text="↓", command=partial(speed_label_change, 0))
    speed_down_but.pack()

    led_test_frame = tkinter.Frame(window)
    led_test_frame.pack(side=tkinter.BOTTOM)

    canvas = tkinter.Canvas(window, height=100, width=100)
    canvas.pack()

    def update():
        canvas.create_rectangle(0, 0, 100, 100, fill=convert_2_hex(led.ledout))
        canvas.after(10, update)

    update()
    window.mainloop()


t2 = threading.Thread(target=tkinter_script)
t2.start()


def led_function():
    while True:
        led.run()


t3 = threading.Thread(target=led_function)
t3.start()