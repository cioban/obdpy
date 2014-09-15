#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '29/08/2014 06:49:15 PM'

from time import sleep, time
import traceback

class OBD_CONTROLLER:
    obd = None
    serial_module = None
    obd_info = {}
    no_conn_string = 'UNABLE TO CONNECT'
    connected = False
    last_liter_time = time()
    liters = 0
    distance = 0
    init_distance = 0
    maf_data = []
    speed_data = []

    def __init__(self, obd=None, serial_module=None):
        self.serial_module = serial_module
        self.obd = obd
        self.obd.pid_dict[0x04].calc_function = self.obd.engine_load
        self.obd.pid_dict[0x05].calc_function = self.obd.get_temp
        self.obd.pid_dict[0x06].calc_function = self.obd.trim_fuel
        self.obd.pid_dict[0x07].calc_function = self.obd.trim_fuel
        self.obd.pid_dict[0x0C].calc_function = self.obd.engine_rpm
        self.obd.pid_dict[0x0D].calc_function = self.obd.speed
        self.obd.pid_dict[0x46].calc_function = self.obd.get_temp
        self.obd.pid_dict[0x31].calc_function = self.obd.distance
        self.obd.pid_dict[0x1F].calc_function = self.obd.runtime
        self.obd.pid_dict[0x10].calc_function = self.obd.maf
        self.obd.pid_dict[0x11].calc_function = self.obd.throttle_position

    def avg(self, value_list):
        value_sum = 0

        for elm in value_list:
            value_sum += elm

        return value_sum/(len(value_list)*1.0)

    def validate_data(self, data, split=True):
        ret = None
        try:
            my_data = data.pop()
            if my_data == self.no_conn_string:
                self.connected = False
            else:
                self.connected = True
            if split == True:
                my_data = my_data.split()
                ret = filter(bool, my_data)
            else:
                ret = [my_data]
        except:
            self.connected = False
            pass

        return ret

    def setup(self):
        ret = False
        if self.serial_module is None:
            return False

        try:
            sermod = self.serial_module
            sermod.send_cmd("ATZ")
            sleep(2)
            sermod.receive_cmd()

            sermod.send_cmd("ATSP0")
            data = sermod.receive_cmd()
            if data.pop() == 'OK':
                ret = True
        except:
            pass

        return ret

    def connect(self):
        # TODO: Use this to test connection
        sermod.send_cmd("0100")
        data = sermod.receive_cmd()
        self.validate_data(data)

    def get_pids(self, mode=0x01):
        pid_base = 0x00
        sermod = self.serial_module
        while True:
            cmd = "%02X%02X" % (mode, pid_base)
            sermod.send_cmd(cmd)
            data = sermod.receive_cmd()
            data = self.validate_data(data)

            if data is None:
                return False

            self.obd.pid_suported(data, pid_base)
            pid_base += 0x20
            if self.obd.pid_dict[pid_base].enable == False:
                break

        return True

    def get_all_pid_data(self, get_pid_lock=True, mode=0x01):
        get_pid_lock=True
        obd = self.obd
        pid_dict = obd.pid_dict
        sermod = self.serial_module

        for pid, pid_obj in pid_dict.iteritems():
            if pid_obj.enable is False:
                continue
            if pid_obj.calc_function is None:
                continue
            try:
                cmd = "%02X%02X" % (mode, pid)
                sermod.send_cmd(cmd)
                data = sermod.receive_cmd()
                data = self.validate_data(data)
                pid_obj.value = pid_obj.calc_function(data)
            except Exception, e:
                traceback.print_exc(e)
                continue

        get_pid_lock=False

    def show_available_pid(self):
        for pid, pid_obj in self.obd.pid_dict.iteritems():
            if pid_obj.enable:
                print(pid_obj)

    def show_pid_value(self):
        for pid, pid_obj in self.obd.pid_dict.iteritems():
            if pid_obj.enable == False:
                continue
            if pid_obj.calc_function is None:
                continue
            print(pid_obj)

    def get_values(self):
        value_dict = {}
        for pid, pid_obj in self.obd.pid_dict.iteritems():
            if pid_obj.enable == False:
                continue
            if pid_obj.calc_function is None:
                continue
            value_dict[pid_obj.obd_pid] = pid_obj.value

        return value_dict

    def get_data_list(self):
        data_list = {}
        speed = self.obd.pid_dict[0x0D].value
        maf = self.obd.pid_dict[0x10].value

        self.maf_data.append(maf)
        self.speed_data.append(speed)

        try:
            data_list['data1'] = []
            km_per_liter_avg = 0
            km_per_liter = 0
            if maf > 0:
                km_per_liter = self.obd.km_per_liter(speed, maf)
            if km_per_liter > 99.99:
                km_per_liter = 99.99

            if len(self.maf_data) > 0:
                avg_speed = self.avg(self.speed_data)
                avg_maf = self.avg(self.maf_data)
                km_per_liter_avg = self.obd.km_per_liter(avg_speed, avg_maf)

            data_list['data1'].append(['Spd: %d Km/h' % self.obd.pid_dict[0x0D].value, False])
            data_list['data1'].append(['RPM: %d ' % self.obd.pid_dict[0x0C].value, False])
            data_list['data1'].append(['Load: %d%% ' % self.obd.pid_dict[0x04].value, False])
            data_list['data1'].append(['Avg %.2f Km/L ' % km_per_liter_avg, True])
            data_list['data1'].append(['> %.2f Km/L <' % km_per_liter, True])
        except Exception, e:
            traceback.print_exc(e)
            data_list['data1'].append(['DATA ERROR', False])

        try:
            data_list['data2'] = []
            data_list['data2'].append(['Run sec: %d' % self.obd.pid_dict[0x1F].value, False])
            data_list['data2'].append(['Eng temp: %d\'C' % self.obd.pid_dict[0x05].value, False])
            data_list['data2'].append(['Air temp: %d\'C' % self.obd.pid_dict[0x46].value, False])
            data_list['data2'].append(['Dist: %dKm' % (self.distance), False])
            data_list['data2'].append(['T spd: %dKm/h  ' % (max(self.speed_data)), False])
        except Exception, e:
            traceback.print_exc(e)
            data_list['data2'].append(['DATA ERROR', False])

        return data_list
