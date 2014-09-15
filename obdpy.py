#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '29/08/2014 07:08:51 PM'

from time import sleep, time, strftime
from sys import exit
import os.path
from os import system
from threading import Thread
import signal
from Queue import Queue
import traceback

try:
    import cPickle as pickle
except:
    import pickle

from lib.obd import OBD
from lib.obd_controller import OBD_CONTROLLER
from lib.obd_pids import PIDS
from lib.serial_module import SERIAL_MODULE
from lib.pcd8544 import PCD8544
from lib.keypad import KEYPAD
from lib.navigation_menu import NAVIGATION_MENU


init_timeout = 10
port = '/dev/rfcomm0'
#port = '/dev/ttyUSB0'
baudrate = '38400'
store_data = True

APP_PATH = os.path.dirname(os.path.realpath(__file__))
data_file_name = 'obdpy.pickle.%s' % strftime("%Y%m%d%H%M%S")
data_file = os.path.join(APP_PATH, 'data', data_file_name)

sermod = None
obd = None
obd_ctrl = None
app = False
running = True
pcd8544 = PCD8544()
keypad = KEYPAD()
navigation_menu = NAVIGATION_MENU(pcd8544)
data_queue = Queue(maxsize=0)

########################################
def kill_handler(sig=None, frame=None):
    global running
    navigation_menu.screen_shutdown()
    running = False

def init_app():
    global obd_ctrl, sermod, obd
    ret = False
    last_time = time()
    try:
        if obd_ctrl is not None:
            del(obd_ctrl)
            obd_ctrl = None

        if sermod is not None:
            del(sermod)
            sermod = None

        if obd is not None:
            del(obd)
            obd = None
        sermod = SERIAL_MODULE(port, baudrate)
        obd = OBD(PIDS)
        obd_ctrl = OBD_CONTROLLER(obd, sermod)
        if not  obd_ctrl.setup():
            return ret

        if not obd_ctrl.get_pids():
            return ret

        ret = True
    except:
        sermod = None
        obd = None
        obd_ctrl = None

    return ret

def queue_data():
    global obd_ctrl, data_queue
    values = obd_ctrl.get_values()
    data_queue.put([time(), values])

def do_store_data(obd_ctrl, data_file, data_queue):
    data_list = []

    if os.path.exists(data_file):
        data_file_fd = open(data_file, 'rb')
        data_list = pickle.load(data_file_fd)
        data_file_fd.close()

    while data_queue.empty() == False:
        data_list.append(data_queue.get())
        data_queue.task_done()

    data_file_fd = open(data_file, 'wb')
    pickle.dump(data_list, data_file_fd)
    data_file_fd.close()

########################################

print('##################################################')
print('# OBDPY')
print('##################################################')

signal.signal(signal.SIGTERM, kill_handler)


last_time_queue = last_time_init = last_time_store = last_time_show = last_time_get = last_time_clock = time()
init = False
last_serial_ok = False
serial_ok = os.path.exists(port)
user_ok = False
data_list = None
get_pid_lock = False
while True:
    try:
        if running == False:
            break

        sleep(0.1)

        keypad.read()
        if navigation_menu.poll(data_list, keypad.key_value) == False:
            break

        if (not init) and ((time() - last_time_clock) > 1):
            navigation_menu.last_menu_pos = -1
            last_time_clock = time()

        if navigation_menu.lock:
            if (last_serial_ok != serial_ok) and serial_ok:
                navigation_menu.menu_enable_screen('wait_bt', False)
                navigation_menu.menu_lock_screen('wait_bt', False)
                navigation_menu.menu_pos_up()
		navigation_menu.force_clean = True
                serial_ok = last_serial_ok = True
            else:
                serial_ok = os.path.exists(port)

            if serial_ok and keypad.key_value['hash'] and not user_ok:
                navigation_menu.menu_enable_screen('enable', False)
                navigation_menu.menu_lock_screen('enable', False)
                navigation_menu.menu_pos_up()
                user_ok = True

            continue

        if (init == False) and ((time() - last_time_init) > 5):
            init = init_app()
            last_time_init = time()

        if init:
            if (time() - last_time_get) > 0.2:
                if not get_pid_lock:
                    #pid_thread = Thread(target=obd_ctrl.get_all_pid_data, args=(get_pid_lock))
                    #pid_thread.start()
                    obd_ctrl.get_all_pid_data()
                    if store_data == True:
                        queue_data()
                last_time_get = time()

            if (time() - last_time_show) > 0.5:
                #obd_ctrl.show_pid_value()
                data_list = obd_ctrl.get_data_list()
                navigation_menu.last_menu_pos = -1
                last_time_show = time()

            if (time() - last_time_store) > 10:
                if store_data == True:
                    thread = Thread(target=do_store_data, args=(obd_ctrl, data_file, data_queue))
                    thread.start()
                last_time_store = time()

    except KeyboardInterrupt:
        kill_handler()
    except Exception, e:
        traceback.print_exc(e)
        navigation_menu.screen_error()
        exit(0)
    #    print('Error: %s' % str(e))

do_store_data(obd_ctrl, data_file, data_queue)
