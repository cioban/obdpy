#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '10/09/2014 09:32:14 AM'

import os
from time import time,  strftime

class NAVIGATION_MENU:
    lcd = None
    asterisk_old = False
    start_hold_time = 0
    shutdown_time = 3
    lock = True
    force_clean = False

    menu_screens = [
        {'name': 'wait_bt', 'enable': True, 'lock': True },
        {'name': 'enable', 'enable': True, 'lock': True },
        {'name': 'init', 'enable': True, 'lock': False },
        {'name': 'data1', 'enable': True, 'lock': False },
        {'name': 'data2', 'enable': True, 'lock': False },
        ]
    menu_pos = 0
    last_menu_pos = -1

    def __init__(self, lcd):
        self.lcd = lcd

    def menu_pos_common(self, up):
        while True:
            if self.menu_pos < 0:
                self.menu_pos = len(self.menu_screens) - 1
            if self.menu_pos >= len(self.menu_screens):
                self.menu_pos = 0

            screen_data = self.get_screen_data(screen_id=self.menu_pos)
            if screen_data['enable']:
                self.lock = screen_data['lock']
                break

            if up:
                self.menu_pos += 1
            else:
                self.menu_pos -= 1

        if not self.lock:
            self.lcd.cls()
            self.lcd.set_display_mode()

    def menu_pos_up(self):
        screen_data = self.get_screen_data(screen_id=self.menu_pos)
        if not screen_data['lock']:
            self.menu_pos += 1
            self.lock = False
        else:
            self.lock = True

        self.menu_pos_common(up=True)

    def menu_pos_down(self):
        screen_data = self.get_screen_data(screen_id=self.menu_pos)
        if not screen_data['lock']:
            self.menu_pos -= 1
            self.lock = False
        else:
            self.lock = True

        self.menu_pos_common(up=False)

    def get_screen_data(self, screen_id=None, screen_name=None):
        screen_data = None
        if screen_id is None and screen_name is None:
            return None

        try:
            if screen_id is not None and screen_id >= 0:
                screen_data = self.menu_screens[screen_id]
            else:
                for data in self.menu_screens:
                    if data['name'] == screen_name:
                        screen_data = data
                        break
        except:
            pass

        return screen_data

    def menu_lock_screen(self, my_screen_name=None, my_lock=False):
        try:
            screen_data = self.get_screen_data(screen_name=my_screen_name)
            screen_data['lock'] = my_lock
        except:
            pass

    def menu_enable_screen(self, my_screen_name=None, my_enable=False):
        try:
            screen_data = self.get_screen_data(screen_name=my_screen_name)
            screen_data['enable'] = my_enable
        except:
            pass

    def poll(self, data_list=None, key_value=None):
        if key_value is None:
            return

        for key, value in key_value.iteritems():
            if key == 'asterisk':
                if self.asterisk_old != value:
                    self.asterisk_old = value
                    if value is True:
                        self.start_hold_time = time()

                if value is True and ((time() - self.start_hold_time) >= self.shutdown_time):
                    os.system('(sleep 1; shutdown -h now) &')
                    self.screen_shutdown()
                    return False
            else:
                if value is True:
                    if key == 'six':
                        self.menu_pos_up()
                    elif key == 'four':
                        self.menu_pos_down()
                    elif key == 'five' and value is True:
                        self.last_menu_pos = -1
                    #else:
                    #    self.lcd.centre_word(5,'Invalid key!')

        if self.menu_pos == self.last_menu_pos:
            return True

        screen_data = self.get_screen_data(screen_id=self.menu_pos)
        if screen_data is None:
            self.screen_error()
            return False

        screen_name = screen_data['name']
        self.last_menu_pos = self.menu_pos

        if self.force_clean:
            self.force_clean = False
            self.lcd.cls()

        menu_function = eval('self.screen_'+screen_name)
        return menu_function(data_list)


    def common_screen_date(self):
        date = strftime("%d/%m/%Y")
        time = strftime("%H:%M:%S")
        self.lcd.centre_word(4,date)
        self.lcd.centre_word(5,time)

    def screen_wait_bt(self, data_list=None):
        self.lcd.centre_word(0, ":obdpy:")
        self.lcd.centre_word(2, "Waiting for")
        self.lcd.centre_word(3, "serial port")
        self.common_screen_date()
        return True

    def screen_enable(self, data_list=None):
        self.lcd.centre_word(0, ":obdpy:")
        self.lcd.centre_word(2, "Waiting for")
        self.lcd.centre_word(3, "hash key")
        self.common_screen_date()
        return True

    def screen_init(self, data_list=None):
        self.lcd.centre_word(0,":obdpy: ready")
        self.lcd.centre_word(2,"Use keys")
        self.common_screen_date()
        return True

    def screen_data1(self, data_list=None):
        self.lcd.centre_word(0, ":obd: data 1")

        screen_data = None
        try:
            screen_data = data_list['data1']
        except:
            pass
        if screen_data is None:
            self.lcd.centre_word(2, "NO DATA!")
        else:
            line = 1
            for line_data in screen_data:
                try:
                    tag = line_data[0]
                    centre = line_data[1]
                    if centre:
                        self.lcd.centre_word(line,"%s" % tag)
                    else:
                        self.lcd.gotoxy(0,line)
                        self.lcd.text("%s" % tag)
                    line += 1
                except:
                    self.lcd.centre_word(line, "DATA ERROR!")

        return True

    def screen_data2(self, data_list=None):
        self.lcd.centre_word(0, ":obd: data 2")

        screen_data = None
        try:
            screen_data = data_list['data2']
        except:
            pass
        if screen_data is None:
            self.lcd.centre_word(2, "NO DATA!")
        else:
            line = 1
            for line_data in screen_data:
                try:
                    tag = line_data[0]
                    centre = line_data[1]
                    if centre:
                        self.lcd.centre_word(line,"%s" % tag)
                    else:
                        self.lcd.gotoxy(0,line)
                        self.lcd.text("%s" % tag)
                    line += 1
                except:
                    self.lcd.centre_word(line, "DATA ERROR!")

        return True

    def screen_shutdown(self):
        self.lcd.cls()
        self.lcd.set_display_mode(invert=True)
        self.lcd.centre_word(1,":obdpy:")
        self.lcd.centre_word(3,"turning off")

    def screen_error(self):
        self.lcd.cls()
        self.lcd.set_display_mode(invert=True)
        self.lcd.centre_word(1,":obdpy:")
        self.lcd.centre_word(3,"ERROR ERROR")
        self.lcd.centre_word(5,"ERROR ERROR")

if __name__ == '__main__':
    from pcd8544 import PCD8544
    from keypad import KEYPAD
    from time import sleep

    lcd = PCD8544()
    keypad = KEYPAD()
    nav_menu = NAVIGATION_MENU(lcd)

    my_data = None

    try:
        while True:

            keypad.read()
            if nav_menu.poll(data_list=my_data, key_value=keypad.key_value) is False:
                break
            sleep(0.2)
    except KeyboardInterrupt:
        pass
    #except Exception, e:
    #    print "ERROR:", str(e)

    nav_menu.screen_shutdown()
