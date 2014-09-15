#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '06/08/2014 08:29:22 PM'

from sys import stdout
import serial
from time import time

class SERIAL_MODULE:
    dev = None
    received_buffer = ''
    receive_timeout = 1 # seconds

    def __init__(self, port, baudrate):
        bytesize = serial.EIGHTBITS
        parity = serial.PARITY_NONE
        stopbits = serial.STOPBITS_ONE
        timeout=0.1
        xonxoff=0
        rtscts=0

        self.dev = serial.Serial(port, baudrate,
            bytesize, parity, stopbits, timeout, xonxoff, rtscts)
        self.dev.flushInput()
        self.dev.flushOutput()

    def flush_all(self):
        self.dev.flushInput()
        self.dev.flushOutput()
        self.received_buffer = ''

    def send_cmd(self, cmd=0):
        self.flush_all()
        #stdout.write('SEND: ')
        #self.printByte(cmd)
        if cmd != 0:
            self.dev.write(cmd+'\r')

    def printByte(self, char_array):
        for TT in char_array:
            #aux = "0x%02X" % ord(TT)
            aux = "%02X" % ord(TT)
            stdout.write(aux + " ")
        stdout.write("\n")

    def receive_cmd(self):
        data = None
        try:
            read_time = time()
            self.received_buffer = ''
            while True:
                data = self.dev.read(1)
                if data == ">":
                    break;
                self.received_buffer += data
                if (time() - read_time) > self.receive_timeout:
                    return None

            data = self.received_buffer.split('\r')
            data = filter(bool, data)
        except:
            pass

        return data


if __name__ == '__main__':
    from time import sleep

    port = '/dev/rfcomm0'
    baudrate = '38400'
    sermod = SERIAL_MODULE(port, baudrate)

    def obd_init():
        sermod.send_cmd("ATZ")
        sleep(2)
        print sermod.receive_cmd()

        sermod.send_cmd("ATSP0")
        print sermod.receive_cmd()

        #sermod.send_cmd("ATI")
        #print sermod.receive_cmd()

        sermod.send_cmd("0100")
        print sermod.receive_cmd()

        print('----------')
        print('----------')
        print('----------')
        print('----------')

        sermod.send_cmd("0100")
        print sermod.receive_cmd()

        sermod.send_cmd("0120")
        print sermod.receive_cmd()

        sermod.send_cmd("0140")
        print sermod.receive_cmd()

        sermod.send_cmd("0131")
        print sermod.receive_cmd()

        sermod.send_cmd("0146")
        print sermod.receive_cmd()

        #sermod.send_cmd("0111")
        #print sermod.receive_cmd()
        #sermod.send_cmd("010C")
        #print sermod.receive_cmd()

    obd_init()

#    sleep(1)
#    try:
#        while True:
#            sermod.send_cmd("0111")
#            print sermod.receive_cmd()
#            #sermod.send_cmd("010C")
#            #print sermod.receive_cmd()
#            sleep(0.5)
#    except KeyboardInterrupt:
#        exit(0)


'''
ATZ
OK

ATSP0
OK

ATSP0
OK

ATSP0
OK

ATSP0
OK

'''
