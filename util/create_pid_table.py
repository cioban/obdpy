#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '24/08/2014 10:25:58 AM'


import csv

print('PIDS = {')

with open('pid.csv', 'r') as csvfile:
    obd_pid_data = csv.reader(csvfile)
    for row in obd_pid_data:
        pid_info = filter(bool, row)

        if len(pid_info) < 4:
            formula = ''
        else:
            formula = pid_info.pop()
            formula = formula.replace('\n', ' - ')
            formula = formula.replace('\'', '-')


        pid = 0
        try:
            pid = int(pid_info[0], 16)
        except:
            pid = int(pid_info[0])

        try:
            length = int(pid_info[1])
        except:
            continue

        desc = pid_info[2].replace('\n', ' - ')
        desc = desc.replace('\'', '-')

        #'00': PID('00', 4, 'PIDs supported [01 - 20]', 'Bit encoded [A7..D0] == [PID $01..PID $20] See below'),
        print "    %d: PID(%d, %d, '%s', '%s')," % (pid, pid, length, desc, formula)

print('}')
