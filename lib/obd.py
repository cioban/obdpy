#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '24/08/2014 11:02:34 AM'

class OBD:
    pid_dict = None
    gasoline_density = 710 # grams/liter

    def __init__(self, pid_dict=None):
        self.pid_dict = pid_dict

    def filter_data(self, data):
        data = filter(bool, data)
        ret = data.pop()
        return ret.split()

    def pid_suported(self, data_list, pid_base=0):
        try:
            data_len = self.pid_dict[pid_base].length
            if data_len == None or data_len == 0:
                return
        except:
            return
        data_list = data_list[-data_len:]
        data = 0
        shift_count = 3
        for hex_num in data_list:
            data |= (int(hex_num, 16) << (shift_count * 8))
            shift_count = shift_count - 1

        pid_base += 1
        comp = 0x80000000
        while (comp > 0):
            if data & comp:
                self.pid_dict[pid_base].enable = 1
            pid_base += 1
            comp >>= 1

    # PID: 0x04
    def engine_load(self, data):
        # A*100/255  in %
        load_data = int(data.pop(), 16)
        load = (load_data * 100)/255
        return load

    # PID: 0x05 and PID: 0x46
    def get_temp(self, data):
        # A-40 % Celsius
        temp_data = int(data.pop(), 16)
        return temp_data - 40

    # PID: 0x0C
    def engine_rpm(self, data):
        # ((A*256)+B)/4
        rpm_data_b = int(data.pop(), 16)
        rpm_data_a = int(data.pop(), 16)
        rpm =  ((rpm_data_a * 256) + rpm_data_b) / 4
        return rpm

    # PID: 0x0D
    def speed(self, data):
        # A in Km/h
        return int(data.pop(), 16)

    def distance(self, data):
        # (A*256)+B in Km
        data_b = int(data.pop(), 16)
        data_a = int(data.pop(), 16)
        return (data_a * 256) + data_b

    def maf(sef, data):
        # ((A*256)+B) / 100
        data_b = int(data.pop(), 16)
        data_a = int(data.pop(), 16)
        return ((data_a * 256) + data_b) / 100

    def runtime(self, data):
        # (A*256)+B
        data_b = int(data.pop(), 16)
        data_a = int(data.pop(), 16)
        return (data_a * 256) + data_b

    def trim_fuel(self, data):
        # (A-128) * 100/128
        data_a = int(data.pop(), 16)
        return (data_a - 128) * 100/128

    def throttle_position(self, data):
        # A*100/255
        data_a = int(data.pop(), 16)
        return (data_a * 100)/255

    #PIDs 0x14 and 0x15
    def bank_sensor(self, data):
        # This sensor gives 2 values, but only the oxygen is used in obdpy
        # 2 values: A/200 in volts and (B-128) * 100/128 in %
        data_b = int(data.pop(), 16)
        data_a = int(data.pop(), 16)
        return data_a/200

    def km_per_liter(self, speed, maf):
        # maf: Mass Air Flow - The mass of Air in grams per second consumed.
        # speed: the vehicle in Km/h

        # Links:
        # http://www.windmill.co.uk/obdii.pdf
        # http://www.windmill.co.uk/fuel.html
        # http://www.mp3car.com/engine-management-obd-ii-engine-diagnostics-etc/75138-calculating-mpg-from-vss-and-maf-from-obd2.html
        # http://www.investidorpetrobras.com.br/pt/servicos/formulas-de-conversao/detalhe-formulas-de-conversao/densidade-e-poderes-calorificos-superiores.htm
        # http://en.wikipedia.org/wiki/Gasoline

        # Constants
        # Air to gasoline ideal ratio: 14.7 grams of air to 1 gram of gasoline
        # The minimal gasoline density: 710 grams/liter

        # Steps:
        #   1 - Divide the MAF by 14.7 to get grams of fuel per second
        #   2 - Divide result by 710 to get liters of fuel per second
        #   3 - Multiply result by 3600 to get liters per hour
        #   4 - To get Km per liter, divide speed by liters per hour

        if speed == 0 or maf == 0:
            return 0

        liters_per_hour = ( (maf / 14.7) / self.gasoline_density ) * 3600
        km_per_liter = speed / liters_per_hour

        return km_per_liter

    def maf_liters(self, maf):
        return (maf / 14.7) / (self.gasoline_density)

'''
PID:[1] STR_PID:['01'] LEN:[4] DESC:[Monitor status since DTCs cleared. (Includes malfunction indicator lamp (MIL) status and number of DTCs.)]
PID:[3] STR_PID:['03'] LEN:[2] DESC:[Fuel system status]
PID:[4] STR_PID:['04'] LEN:[1] DESC:[Calculated engine load value]
PID:[5] STR_PID:['05'] LEN:[1] DESC:[Engine coolant temperature]
PID:[6] STR_PID:['06'] LEN:[1] DESC:[Short term fuel % trim—Bank 1]
PID:[7] STR_PID:['07'] LEN:[1] DESC:[Long term fuel % trim—Bank 1]
PID:[12] STR_PID:['0C'] LEN:[2] DESC:[Engine RPM]
PID:[13] STR_PID:['0D'] LEN:[1] DESC:[Vehicle speed]
PID:[14] STR_PID:['0E'] LEN:[1] DESC:[Timing advance]
PID:[15] STR_PID:['0F'] LEN:[1] DESC:[Intake air temperature]
PID:[16] STR_PID:['10'] LEN:[2] DESC:[MAF air flow rate]
PID:[17] STR_PID:['11'] LEN:[1] DESC:[Throttle position]
PID:[19] STR_PID:['13'] LEN:[1] DESC:[Oxygen sensors present]
PID:[20] STR_PID:['14'] LEN:[2] DESC:[Bank 1, Sensor 1: - Oxygen sensor voltage, - Short term fuel trim]
PID:[21] STR_PID:['15'] LEN:[2] DESC:[Bank 1, Sensor 2: - Oxygen sensor voltage, - Short term fuel trim]
PID:[28] STR_PID:['1C'] LEN:[1] DESC:[OBD standards this vehicle conforms to]
PID:[31] STR_PID:['1F'] LEN:[2] DESC:[Run time since engine start]

PID:[33] STR_PID:['21'] LEN:[2] DESC:[Distance traveled with malfunction indicator lamp (MIL) on]
PID:[46] STR_PID:['2E'] LEN:[1] DESC:[Commanded evaporative purge]
PID:[48] STR_PID:['30'] LEN:[1] DESC:[# of warm-ups since codes cleared]
PID:[49] STR_PID:['31'] LEN:[2] DESC:[Distance traveled since codes cleared]
PID:[64] STR_PID:['40'] LEN:[4] DESC:[PIDs supported [41 - 60]]
PID:[66] STR_PID:['42'] LEN:[2] DESC:[Control module voltage]
PID:[67] STR_PID:['43'] LEN:[2] DESC:[Absolute load value]
PID:[68] STR_PID:['44'] LEN:[2] DESC:[Command equivalence ratio]
PID:[69] STR_PID:['45'] LEN:[1] DESC:[Relative throttle position]
PID:[70] STR_PID:['46'] LEN:[1] DESC:[Ambient air temperature]
PID:[71] STR_PID:['47'] LEN:[1] DESC:[Absolute throttle position B]
PID:[76] STR_PID:['4C'] LEN:[1] DESC:[Commanded throttle actuator]

'''


'''
SEND: 30 31 30 30 
['0100', '41 00 BE 1F B8 13 ']
SEND: 30 31 32 30 
['0120', '41 20 80 05 80 01 ']
SEND: 30 31 34 30 
['0140', '41 40 7E 10 00 00 ']
SEND: 30 31 33 31 
['0131', '41 31 11 00 ']
SEND: 30 31 34 36 
['0146', '41 46 3A ']
'''

if __name__ == '__main__':
    from obd_pids import PIDS
    obd = OBD(PIDS)
    #my_data = ['0100', '41 00 BE 1F B8 13 ', '', '']
    #my_data = ['0120', '41 20 80 05 80 01 ']
    my_data = ['0140', '41 40 7E 10 00 00 ']
    data = obd.filter_data(my_data)
    obd.pid_suported(data, 0x40)
    for pid, pid_obj in obd.pid_dict.iteritems():
        if pid_obj.enable:
            print(pid_obj)

    #print obd.engine_load(['AA'])
    #print obd.get_temp(['AA'])
    #print obd.engine_rpm(['AA', 'AA'])
    #print obd.speed(['AA'])
    print obd.distance(['11', '00'])
