#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '21/08/2014 07:02:17 PM'



class PID:
    enable = False
    obd_pid = None
    length = 0
    description = None
    formula_hint = None
    calc_function = None
    value = 0
    unit = ''
    def __init__(self, obd_pid, length, description, formula_hint, unit='', calc_function=None):
        self.obd_pid = obd_pid
        self.obd_pid_str = '%02X' % obd_pid
        self.length = length
        self.description = description
        self.formula_hint = formula_hint
        self.calc_function = calc_function
        self.unit = unit

    def __str__(self):
        return "PID:[%d] STR_PID:['%s'] LEN:[%d] DESC:[%s] VALUE:[%s]" % (self.obd_pid, self.obd_pid_str, self.length, self.description, str(self.value))

# From: http://en.wikipedia.org/wiki/OBD-II_PIDs
PIDS = {
    0: PID(0, 4, 'PIDs supported [01 - 20]', 'Bit encoded [A7..D0] == [PID $01..PID $20] See below'),
    1: PID(1, 4, 'Monitor status since DTCs cleared. (Includes malfunction indicator lamp (MIL) status and number of DTCs.)', 'Bit encoded. See below'),
    2: PID(2, 2, 'Freeze DTC', ''),
    3: PID(3, 2, 'Fuel system status', 'Bit encoded. See below'),
    4: PID(4, 1, 'Calculated engine load value', 'A*100/255', '%'),
    5: PID(5, 1, 'Engine coolant temperature', 'A-40', '\'C'),
    6: PID(6, 1, 'Short term fuel % trim—Bank 1', '(A-128) * 100/128', '%'),
    7: PID(7, 1, 'Long term fuel % trim—Bank 1', '(A-128) * 100/128', '%'),
    8: PID(8, 1, 'Short term fuel % trim—Bank 2', '(A-128) * 100/128', '%'),
    9: PID(9, 1, 'Long term fuel % trim—Bank 2', '(A-128) * 100/128', '%'),
    10: PID(10, 1, 'Fuel pressure', 'A*3'),
    11: PID(11, 1, 'Intake manifold absolute pressure', 'A'),
    12: PID(12, 2, 'Engine RPM', '((A*256)+B)/4', 'RPM'),
    13: PID(13, 1, 'Vehicle speed', 'A', 'Km/h'),
    14: PID(14, 1, 'Timing advance', '(A-128)/2'),
    15: PID(15, 1, 'Intake air temperature', 'A-40', '\'C'),
    16: PID(16, 2, 'MAF air flow rate', '((A*256)+B) / 100', 'grams/sec'),
    17: PID(17, 1, 'Throttle position', 'A*100/255', '%'),
    18: PID(18, 1, 'Commanded secondary air status', 'Bit encoded. See below'),
    19: PID(19, 1, 'Oxygen sensors present', '[A0..A3] == Bank 1, Sensors 1-4. [A4..A7] == Bank 2...'),
    20: PID(20, 2, 'Bank 1, Sensor 1: - Oxygen sensor voltage, - Short term fuel trim', 'A/200 - (B-128) * 100/128 (if B==$FF, sensor is not used in trim calc)'),
    21: PID(21, 2, 'Bank 1, Sensor 2: - Oxygen sensor voltage, - Short term fuel trim', 'A/200 - (B-128) * 100/128 (if B==$FF, sensor is not used in trim calc)'),
    22: PID(22, 2, 'Bank 1, Sensor 3: - Oxygen sensor voltage, - Short term fuel trim', 'A/200 - (B-128) * 100/128 (if B==$FF, sensor is not used in trim calc)'),
    23: PID(23, 2, 'Bank 1, Sensor 4: - Oxygen sensor voltage, - Short term fuel trim', 'A/200 - (B-128) * 100/128 (if B==$FF, sensor is not used in trim calc)'),
    24: PID(24, 2, 'Bank 2, Sensor 1: - Oxygen sensor voltage, - Short term fuel trim', 'A/200 - (B-128) * 100/128 (if B==$FF, sensor is not used in trim calc)'),
    25: PID(25, 2, 'Bank 2, Sensor 2: - Oxygen sensor voltage, - Short term fuel trim', 'A/200 - (B-128) * 100/128 (if B==$FF, sensor is not used in trim calc)'),
    26: PID(26, 2, 'Bank 2, Sensor 3: - Oxygen sensor voltage, - Short term fuel trim', 'A/200 - (B-128) * 100/128 (if B==$FF, sensor is not used in trim calc)'),
    27: PID(27, 2, 'Bank 2, Sensor 4: - Oxygen sensor voltage, - Short term fuel trim', 'A/200 - (B-128) * 100/128 (if B==$FF, sensor is not used in trim calc)'),
    28: PID(28, 1, 'OBD standards this vehicle conforms to', 'Bit encoded. See below'),
    29: PID(29, 1, 'Oxygen sensors present', 'Similar to PID 13, but [A0..A7] == [B1S1, B1S2, B2S1, B2S2, B3S1, B3S2, B4S1, B4S2]'),
    30: PID(30, 1, 'Auxiliary input status', 'A0 == Power Take Off (PTO) status (1 == active) - [A1..A7] not used'),
    31: PID(31, 2, 'Run time since engine start', '(A*256)+B', 'sec'),
    32: PID(32, 4, 'PIDs supported [21 - 40]', 'Bit encoded [A7..D0] == [PID $21..PID $40] See below'),
    33: PID(33, 2, 'Distance traveled with malfunction indicator lamp (MIL) on', '(A*256)+B'),
    34: PID(34, 2, 'Fuel Rail Pressure (relative to manifold vacuum)', '((A*256)+B) * 0.079'),
    35: PID(35, 2, 'Fuel Rail Pressure (diesel, or gasoline direct inject)', '((A*256)+B) * 10'),
    36: PID(36, 4, 'O2S1_WR_lambda(1): - Equivalence Ratio - Voltage', '((A*256)+B)*2/65535 or ((A*256)+B)/32768 - ((C*256)+D)*8/65535 or ((C*256)+D)/8192'),
    37: PID(37, 4, 'O2S2_WR_lambda(1): - Equivalence Ratio - Voltage', '((A*256)+B)*2/65535 - ((C*256)+D)*8/65535'),
    38: PID(38, 4, 'O2S3_WR_lambda(1): - Equivalence Ratio - Voltage', '((A*256)+B)*2/65535 - ((C*256)+D)*8/65535'),
    39: PID(39, 4, 'O2S4_WR_lambda(1): - Equivalence Ratio - Voltage', '((A*256)+B)*2/65535 - ((C*256)+D)*8/65535'),
    40: PID(40, 4, 'O2S5_WR_lambda(1): - Equivalence Ratio - Voltage', '((A*256)+B)*2/65535 - ((C*256)+D)*8/65535'),
    41: PID(41, 4, 'O2S6_WR_lambda(1): - Equivalence Ratio - Voltage', '((A*256)+B)*2/65535 - ((C*256)+D)*8/65535'),
    42: PID(42, 4, 'O2S7_WR_lambda(1): - Equivalence Ratio - Voltage', '((A*256)+B)*2/65535 - ((C*256)+D)*8/65535'),
    43: PID(43, 4, 'O2S8_WR_lambda(1): - Equivalence Ratio - Voltage', '((A*256)+B)*2/65535 - ((C*256)+D)*8/65535'),
    44: PID(44, 1, 'Commanded EGR', 'A*100/255'),
    45: PID(45, 1, 'EGR Error', '(A-128) * 100/128'),
    46: PID(46, 1, 'Commanded evaporative purge', 'A*100/255'),
    47: PID(47, 1, 'Fuel Level Input', 'A*100/255'),
    48: PID(48, 1, '# of warm-ups since codes cleared', 'A'),
    49: PID(49, 2, 'Distance traveled since codes cleared', '(A*256)+B', 'Km'),
    50: PID(50, 2, 'Evap. System Vapor Pressure', '((A*256)+B)/4 (A and B are two-s complementsigned)'),
    51: PID(51, 1, 'Barometric pressure', 'A'),
    52: PID(52, 4, 'O2S1_WR_lambda(1): - Equivalence Ratio - Current', '((A*256)+B)/32,768 - ((C*256)+D)/256 - 128'),
    53: PID(53, 4, 'O2S2_WR_lambda(1): - Equivalence Ratio - Current', '((A*256)+B)/32,768 - ((C*256)+D)/256 - 128'),
    54: PID(54, 4, 'O2S3_WR_lambda(1): - Equivalence Ratio - Current', '((A*256)+B)/32768 - ((C*256)+D)/256 - 128'),
    55: PID(55, 4, 'O2S4_WR_lambda(1): - Equivalence Ratio - Current', '((A*256)+B)/32,768 - ((C*256)+D)/256 - 128'),
    56: PID(56, 4, 'O2S5_WR_lambda(1): - Equivalence Ratio - Current', '((A*256)+B)/32,768 - ((C*256)+D)/256 - 128'),
    57: PID(57, 4, 'O2S6_WR_lambda(1): - Equivalence Ratio - Current', '((A*256)+B)/32,768 - ((C*256)+D)/256 - 128'),
    58: PID(58, 4, 'O2S7_WR_lambda(1): - Equivalence Ratio - Current', '((A*256)+B)/32,768 - ((C*256)+D)/256 - 128'),
    59: PID(59, 4, 'O2S8_WR_lambda(1): - Equivalence Ratio - Current', '((A*256)+B)/32,768 - ((C*256)+D)/256 - 128'),
    60: PID(60, 2, 'Catalyst Temperature - Bank 1, Sensor 1', '((A*256)+B)/10 - 40'),
    61: PID(61, 2, 'Catalyst Temperature - Bank 2, Sensor 1', '((A*256)+B)/10 - 40'),
    62: PID(62, 2, 'Catalyst Temperature - Bank 1, Sensor 2', '((A*256)+B)/10 - 40'),
    63: PID(63, 2, 'Catalyst Temperature - Bank 2, Sensor 2', '((A*256)+B)/10 - 40'),
    64: PID(64, 4, 'PIDs supported [41 - 60]', 'Bit encoded [A7..D0] == [PID $41..PID $60] See below'),
    65: PID(65, 4, 'Monitor status this drive cycle', 'Bit encoded. See below'),
    66: PID(66, 2, 'Control module voltage', '((A*256)+B)/1000', 'V'),
    67: PID(67, 2, 'Absolute load value', '((A*256)+B)*100/255'),
    68: PID(68, 2, 'Command equivalence ratio', '((A*256)+B)/32768'),
    69: PID(69, 1, 'Relative throttle position', 'A*100/255'),
    70: PID(70, 1, 'Ambient air temperature', 'A-40', '\'C'),
    71: PID(71, 1, 'Absolute throttle position B', 'A*100/255'),
    72: PID(72, 1, 'Absolute throttle position C', 'A*100/255'),
    73: PID(73, 1, 'Accelerator pedal position D', 'A*100/255'),
    74: PID(74, 1, 'Accelerator pedal position E', 'A*100/255'),
    75: PID(75, 1, 'Accelerator pedal position F', 'A*100/255'),
    76: PID(76, 1, 'Commanded throttle actuator', 'A*100/255'),
    77: PID(77, 2, 'Time run with MIL on', '(A*256)+B'),
    78: PID(78, 2, 'Time since trouble codes cleared', '(A*256)+B'),
    79: PID(79, 4, 'Maximum value for equivalence ratio, oxygen sensor voltage, oxygen sensor current, and intake manifold absolute pressure', 'A, B, C, D*10'),
    80: PID(80, 4, 'Maximum value for air flow rate from mass air flow sensor', 'A*10, B, C, and D are reserved for future use'),
    81: PID(81, 1, 'Fuel Type', 'From fuel type table see below'),
    82: PID(82, 1, 'Ethanol fuel %', 'A*100/255'),
    83: PID(83, 2, 'Absolute Evap system Vapor Pressure', '((A*256)+B)/200'),
    84: PID(84, 2, 'Evap system vapor pressure', '((A*256)+B)-32767'),
    85: PID(85, 2, 'Short term secondary oxygen sensor trim bank 1 and bank 3', '(A-128)*100/128 - (B-128)*100/128'),
    86: PID(86, 2, 'Long term secondary oxygen sensor trim bank 1 and bank 3', '(A-128)*100/128 - (B-128)*100/128'),
    87: PID(87, 2, 'Short term secondary oxygen sensor trim bank 2 and bank 4', '(A-128)*100/128 - (B-128)*100/128'),
    88: PID(88, 2, 'Long term secondary oxygen sensor trim bank 2 and bank 4', '(A-128)*100/128 - (B-128)*100/128'),
    89: PID(89, 2, 'Fuel rail pressure (absolute)', '((A*256)+B) * 10'),
    90: PID(90, 1, 'Relative accelerator pedal position', 'A*100/255'),
    91: PID(91, 1, 'Hybrid battery pack remaining life', 'A*100/255'),
    92: PID(92, 1, 'Engine oil temperature', 'A - 40'),
    93: PID(93, 2, 'Fuel injection timing', '(((A*256)+B)-26,880)/128'),
    94: PID(94, 2, 'Engine fuel rate', '((A*256)+B)*0.05'),
    95: PID(95, 1, 'Emission requirements to which vehicle is designed', 'Bit Encoded'),
    96: PID(96, 4, 'PIDs supported [61 - 80]', 'Bit encoded [A7..D0] == [PID $61..PID $80] See below'),
    97: PID(97, 1, 'Driver-s demand engine - percent torque', 'A-125'),
    98: PID(98, 1, 'Actual engine - percent torque', 'A-125'),
    99: PID(99, 2, 'Engine reference torque', 'A*256+B'),
    100: PID(100, 5, 'Engine percent torque data', 'A-125 Idle - B-125 Engine point 1 - C-125 Engine point 2 - D-125 Engine point 3 - E-125 Engine point 4'),
    101: PID(101, 2, 'Auxiliary input / output supported', 'Bit Encoded'),
    102: PID(102, 5, 'Mass air flow sensor', ''),
    103: PID(103, 3, 'Engine coolant temperature', ''),
    104: PID(104, 7, 'Intake air temperature sensor', ''),
    105: PID(105, 7, 'Commanded EGR and EGR Error', ''),
    106: PID(106, 5, 'Commanded Diesel intake air flow control and relative intake air flow position', ''),
    107: PID(107, 5, 'Exhaust gas recirculation temperature', ''),
    108: PID(108, 5, 'Commanded throttle actuator control and relative throttle position', ''),
    109: PID(109, 6, 'Fuel pressure control system', ''),
    110: PID(110, 5, 'Injection pressure control system', ''),
    111: PID(111, 3, 'Turbocharger compressor inlet pressure', ''),
    112: PID(112, 9, 'Boost pressure control', ''),
    113: PID(113, 5, 'Variable Geometry turbo (VGT) control', ''),
    114: PID(114, 5, 'Wastegate control', ''),
    115: PID(115, 5, 'Exhaust pressure', ''),
    116: PID(116, 5, 'Turbocharger RPM', ''),
    117: PID(117, 7, 'Turbocharger temperature', ''),
    118: PID(118, 7, 'Turbocharger temperature', ''),
    119: PID(119, 5, 'Charge air cooler temperature (CACT)', ''),
    120: PID(120, 9, 'Exhaust Gas temperature (EGT) Bank 1', 'Special PID. See below'),
    121: PID(121, 9, 'Exhaust Gas temperature (EGT) Bank 2', 'Special PID. See below'),
    122: PID(122, 7, 'Diesel particulate filter (DPF)', ''),
    123: PID(123, 7, 'Diesel particulate filter (DPF)', ''),
    124: PID(124, 9, 'Diesel Particulate filter (DPF) temperature', ''),
    125: PID(125, 1, 'NOx NTE control area status', ''),
    126: PID(126, 1, 'PM NTE control area status', ''),
    127: PID(127, 13, 'Engine run time', ''),
    128: PID(128, 4, 'PIDs supported [81 - A0]', 'Bit encoded [A7..D0] == [PID $81..PID $A0] See below'),
    129: PID(129, 21, 'Engine run time for Auxiliary Emissions Control Device(AECD)', ''),
    130: PID(130, 21, 'Engine run time for Auxiliary Emissions Control Device(AECD)', ''),
    131: PID(131, 5, 'NOx sensor', ''),
    160: PID(160, 4, 'PIDs supported [A1 - C0]', 'Bit encoded [A7..D0] == [PID $A1..PID $C0] See below'),
    192: PID(192, 4, 'PIDs supported [C1 - E0]', 'Bit encoded [A7..D0] == [PID $C1..PID $E0] See below'),
}

if __name__ == '__main__':
    from pprint import pprint
    for pid, pid_obj in PIDS.iteritems():
        print(pid_obj)
