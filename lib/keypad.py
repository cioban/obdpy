#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '21/05/2013 04:14:36 PM'

import time
import RPi.GPIO as GPIO

class KEYPAD():
    #col_pins = [0, 1, 4]
    col_pins = [25, 11, 4]
    row_pins = [7, 8, 9, 10]
    key_value = {
        'one': False,
        'two': False,
        'three': False,
        'four': False,
        'five': False,
        'six': False,
        'seven': False,
        'eight': False,
        'nine': False,
        'asterisk': False,
        'zero': False,
        'hash': False,
    }

    def __init__(self):
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)
        for pin in self.col_pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        for pin in self.row_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def reset(self):
        for k in self.key_value.iteritems():
            k = False
        for pin in self.col_pins:
            GPIO.output(pin, False)

    def read(self):
        self.reset()

        # COL 1
        GPIO.output(self.col_pins[2], True)
        self.key_value['one'] = bool(GPIO.input(self.row_pins[0]))
        self.key_value['four'] = bool(GPIO.input(self.row_pins[1]))
        self.key_value['seven'] = bool(GPIO.input(self.row_pins[2]))
        self.key_value['asterisk'] = bool(GPIO.input(self.row_pins[3]))

        # COL 2
        GPIO.output(self.col_pins[2], False)
        GPIO.output(self.col_pins[1], True)
        self.key_value['two'] = bool(GPIO.input(self.row_pins[0]))
        self.key_value['five'] = bool(GPIO.input(self.row_pins[1]))
        self.key_value['eight'] = bool(GPIO.input(self.row_pins[2]))
        self.key_value['zero'] = bool(GPIO.input(self.row_pins[3]))

        # COL 3
        GPIO.output(self.col_pins[1], False)
        GPIO.output(self.col_pins[0], True)
        self.key_value['three'] = bool(GPIO.input(self.row_pins[0]))
        self.key_value['six'] = bool(GPIO.input(self.row_pins[1]))
        self.key_value['nine'] = bool(GPIO.input(self.row_pins[2]))
        self.key_value['hash'] = bool(GPIO.input(self.row_pins[3]))
        GPIO.output(self.col_pins[0], False)

        return self.key_value

if __name__ == "__main__":
    from pprint import pprint
    pad = KEYPAD()
    while 1==1:
        print("\x1B[2J")
        pad.read()
        pprint(pad.key_value)
        time.sleep(0.3)

