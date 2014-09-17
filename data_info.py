#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '13/09/2014 22:31:02'

import cPickle as pickle
#import pickle
from sys import argv, exit

from lib.obd_pids import PIDS
from lib.obd import OBD

all_data = {}
avg_data = {}
min_data = {}
max_data = {}
EXCLUDED_PIDS = []
obd = OBD()

def avg(value_list):
    value_sum = 0
    for elm in value_list:
        value_sum += elm
    return value_sum/(len(value_list)*1.0)


print("\x1B[2J")
print('##################################################')
print('# OBDPY DATA INFO')
print('##################################################')

try:
    data_file = argv[1]
except:
    print('Usage: %s <data_file>' % argv[0])
    exit(1)

data_file_fd = open(data_file, 'rb')
data = pickle.load(data_file_fd)
data_file_fd.close()

for data_list in data:
    data_dict = data_list[1]
    for pid, value in data_dict.iteritems():
        try:
            all_data[pid].append(value)
        except:
            all_data[pid] = [value]

print('\n ==> PID DATA')
for pid, all_pid_data in all_data.iteritems():
    pid_obj = PIDS[pid]
    print('[0x%02X] %s' % (pid, pid_obj.description))
    avg_value = avg(all_pid_data)
    min_value = min(all_pid_data)
    max_value = max(all_pid_data)
    print('    * MIN[%d %s] MAX[%d %s] AVG[%.3f %s]' % (min_value, pid_obj.unit, max_value, pid_obj.unit, avg_value, pid_obj.unit))
    avg_data[pid] = avg_value
    min_data[pid] = min_value
    max_data[pid] = max_value

print('\n ==> INFO')
avg_speed = avg_data[0x0D]
avg_maf = avg_data[0x10]
kilometrs_per_liters_avg = obd.km_per_liter(avg_speed, avg_maf)
distance = max_data[0x31] - min_data[0x31]
print('Fuel consumption average (using MAF and Speed): %.3f Km/L' % kilometrs_per_liters_avg)
print('Distance traveled: %d Km' % distance)
liters = 0
for maf in all_data[0x10]:
    liters += obd.maf_liters(maf)
print('Fuel consumption : %.3f Liters' % (liters))
kilometrs_per_liters_avg_alternative = 0
if distance > 0 and liters > 0:
    kilometrs_per_liters_avg_alternative = distance / liters
print('Fuel consumption average (using distance and liters): %.3f Km/L' % kilometrs_per_liters_avg_alternative)

print('\n\n')
