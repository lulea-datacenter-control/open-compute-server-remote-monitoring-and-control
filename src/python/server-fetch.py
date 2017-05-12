#!/usr/bin/env python

#
# Copyright (c) 2017 Martin Eriksson
#		2017 Riccardo Lucchese <riccardo.lucchese@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import datetime
import re
import time
import argparse
import subprocess
import numpy
import scipy
import scipy.io
import shlex
import socket

_COLLECT_DELL = 0
_COLLECT_FB = 1
_MAX_SAMPLING_PERIOD = 100   # [Hz]
_TCP_IP = 'localhost'
_TCP_PORT = 9001
_BUFFER_SIZE = 1024

class data_trace(object):
    def __init__(self, name):
        assert isinstance(name, str)
        assert len(name) > 0

        self._name = name
        self._data = []
        self._time = []

    def get_name(self):
        return self._name
    
    def save_start_time(self, start_time):
        assert isinstance(start_time, float)
        self._start_time = start_time

    def append(self, time, value):
        assert isinstance(time, float)
        assert isinstance(value,float)
        self._time.append(time)
        self._data.append(value)

    def get_time_with_data(self):
        return numpy.array(self._time), numpy.array(self._data)

    def get_last_value(self):
        if len(self._data):
            return self._data[-1]
        return 0

    def get_start_time(self):
        return self._start_time


class server(object):
    def __init__(self, _use_ipmi, _use_snmp, server_choice, conn):
        assert(server_choice in (_COLLECT_DELL, _COLLECT_FB))
        assert(isinstance(_use_ipmi, bool))
        assert(isinstance(_use_snmp, bool))
        self._use_ipmi = _use_ipmi
        self._use_snmp = _use_snmp
        self.server_choice = server_choice
        self.conn = conn

        #
        # table of variables we are going to collect
        # x_i       inlet temperature                       # [tens of degrees Celsius]
        # x_o       exhaust temperature                     # [tens of degrees Celsius]
        # x_j       temperature of the j-th component       # [tens of degrees Celsius]
        # ! j=1 -> CPU 1, j=2 -> CPU 2
        # u_j       speed of the j-th fan                   # [RPM]
        # ! j=1 -> Fan 1, j=2 -> Fan 2, ...
        # t         time vector
        # l_c       CPU load
        # l_io      IO load
        # l_m       Memory load
        # l_s       System load
        #

        self._s_t_ipmi = data_trace('s_t_ipmi')
        self._x_i = data_trace('x_i')	# todo: explain
        self._x_o = data_trace('x_o')
        self._x_s0 = data_trace('x_s0')
        self._x_s1 = data_trace('x_s1')
        self._x_d0 = data_trace('x_d0')
        self._x_d1 = data_trace('x_d1')
        self._u_1 = data_trace('u_1')
        self._u_2 = data_trace('u_2')
        self._u_3 = data_trace('u_3')
        self._u_4 = data_trace('u_4')
        self._u_5 = data_trace('u_5')
        self._u_6 = data_trace('u_6')
        self._l_c = data_trace('l_c')
        self._l_io = data_trace('l_io')
        self._l_m = data_trace('l_m')
        self._l_s = data_trace('l_s')
        self._c_1 = data_trace('c_1')
        self._c_2 = data_trace('c_2')
        self._v_1 = data_trace('v_1')
        self._v_2 = data_trace('v_2')
        self._p_c = data_trace('p_c')

        self._s_t_snmp = data_trace('s_t_snmp')
        self._x_0 = data_trace('x_0')
        self._x_1 = data_trace('x_1')
        self._x_2 = data_trace('x_2')
        self._x_3 = data_trace('x_3')
        self._x_4 = data_trace('x_4')
        self._x_5 = data_trace('x_5')
        self._x_6 = data_trace('x_6')
        self._x_7 = data_trace('x_7')
        self._x_8 = data_trace('x_8')
        self._x_9 = data_trace('x_9')
        self._x_10 = data_trace('x_10')
        self._x_11 = data_trace('x_11')
        self._x_12 = data_trace('x_12')
        self._x_13 = data_trace('x_13')
        self._x_14 = data_trace('x_14')
        self._x_15 = data_trace('x_15')
        self._x_16 = data_trace('x_16')
        self._x_17 = data_trace('x_17')
        self._x_18 = data_trace('x_18')

        self._l_0 = data_trace('l_0')
        self._l_1 = data_trace('l_1')
        self._l_2 = data_trace('l_2')
        self._l_3 = data_trace('l_3')
        self._l_4 = data_trace('l_4')
        self._l_5 = data_trace('l_5')
        self._l_6 = data_trace('l_6')
        self._l_7 = data_trace('l_7')
        self._l_8 = data_trace('l_8')
        self._l_9 = data_trace('l_9')
        self._l_10 = data_trace('l_10')
        self._l_11 = data_trace('l_11')
        self._l_12 = data_trace('l_12')
        self._l_13 = data_trace('l_13')
        self._l_14 = data_trace('l_14')
        self._l_15 = data_trace('l_15')
        self._l_16 = data_trace('l_16')
        self._l_17 = data_trace('l_17')
        self._l_18 = data_trace('l_18')
        self._l_19 = data_trace('l_19')
        self._l_20 = data_trace('l_20')
        self._l_21 = data_trace('l_21')
        self._l_22 = data_trace('l_22')
        self._l_23 = data_trace('l_23')
        self._l_24 = data_trace('l_24')
        self._l_25 = data_trace('l_25')
        self._l_26 = data_trace('l_26')
        self._l_27 = data_trace('l_27')
        self._l_28 = data_trace('l_28')
        self._l_29 = data_trace('l_29')
        self._l_30 = data_trace('l_30')
        self._l_31 = data_trace('l_31')
        
   
    def fetch_snmp(self, meas_t, zero_pwr):
        #
        # issue the snmp queries
        #

        if self.server_choice == _COLLECT_DELL:
            #cmd_fmt = "snmpget -c public -v 2c -Oqv 192.168.21.151 %s" 
            # This command retrieves information from one or multiply OIDsreqested.
            # -c [community string]: By default most SNMP enabled devices uses "public".
            # -v [SNMP version]: SNMP protocol version, "1" or "2c".
            # -OQ Removes the type information when displaying varbind values
            # -Ov Display the varbind value only, not the OID
            # [IP]: IP address of the device.
            
            cmd_fmt = "snmpwalk -c public -v 2c -Oqv 192.168.21.151 %s"
            # This command retrieves all variables in the subtree below the given OID.
            
            mib_x = "IDRAC-MIB-SMIv2::temperatureProbeReading" #OID request for all temp sensors
            # ...temperatureProbeReading.1.1" #OID request for inlet temp
            # ...temperatureProbeReading.1.2" #OID request for exhaust temp
            # ...temperatureProbeReading.1.3" #OID request for CPU 1
            #mib_x_2 = "IDRAC-MIB-SMIv2::temperatureProbeReading.1.4" #OID request for CPU 2
            mib_u = "IDRAC-MIB-SMIv2::coolingDeviceReading" 	 #OID request for all fan speeds
            #mib_u_1 = "IDRAC-MIB-SMIv2::coolingDeviceReading.1.1"	 #OID request for fan1 speed
            #mib_u_2 = "IDRAC-MIB-SMIv2::coolingDeviceReading.1.2"	 #OID request for fan2 speed
            #mib_u_3 = "IDRAC-MIB-SMIv2::coolingDeviceReading.1.3"	 #OID request for fan3 speed
            #mib_u_4 = "IDRAC-MIB-SMIv2::coolingDeviceReading.1.4"	 #OID request for fan4 speed
            #mib_u_5 = "IDRAC-MIB-SMIv2::coolingDeviceReading.1.5"	 #OID request for fan5 speed
            #mib_u_6 = "IDRAC-MIB-SMIv2::coolingDeviceReading.1.6"	 #OID request for fan6 speed
            #mib_c_1 = "IDRAC-MIB-SMIv2::processorDeviceCurrentSpeed.1.1"
            #mib_c_2 = "IDRAC-MIB-SMIv2::processorDeviceCurrentSpeed.1.2"
            #mib_v_1 = "IDRAC-MIB-SMIv2::powerSupplyCurrentInputVoltage.1.1"
            #mib_v_2 = "IDRAC-MIB-SMIv2::powerSupplyCurrentInputVoltage.1.2"
            #mib_p_c = "IDRAC-MIB-SMIv2::powerUsageCumulativeWattage.1.1"

            p = subprocess.Popen(shlex.split(cmd_fmt % mib_x), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            snmp_x, err = p.communicate()
            p = subprocess.Popen(shlex.split(cmd_fmt % mib_u), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            snmp_u, err = p.communicate()


            #
            # Parse the outputs
            #
            def _parse_snmp_temperature(temp_str):
                # The temps are measured in tens of degrees Celsius
                return float(temp_str)/10.

            def _parse_snmp_float(fs_str):
                # The fans are measured in RPM
                return float(fs_str)
            
            lines = snmp_x.splitlines()
            meas_x_i = _parse_snmp_temperature(lines[0])
            meas_x_o = _parse_snmp_temperature(lines[1])
            meas_x_s0 = _parse_snmp_temperature(lines[2])
            meas_x_s1 = _parse_snmp_temperature(lines[3])
            lines = snmp_u.splitlines()
            meas_u_1 = _parse_snmp_float(lines[0])
            meas_u_2 = _parse_snmp_float(lines[1])
            meas_u_3 = _parse_snmp_float(lines[2])
            meas_u_4 = _parse_snmp_float(lines[3])
            meas_u_5 = _parse_snmp_float(lines[4])
            meas_u_6 = _parse_snmp_float(lines[5])
            #meas_c_1 = _parse_snmp_fanspeed(snmp_c_1)
            #meas_c_2 = _parse_snmp_fanspeed(snmp_c_2)
            #meas_v_1 = _parse_snmp_fanspeed(snmp_v_1)
            #meas_v_2 = _parse_snmp_fanspeed(snmp_v_2)
            #meas_p_c = _parse_snmp_fanspeed(snmp_p_c)
            #if zero_pwr == None:
            #    zero_pwr = meas_p_c
            #meas_p_c = meas_p_c - zero_pwr


            self._x_i.append(meas_t,meas_x_i)
            self._x_o.append(meas_t,meas_x_o)
            self._x_s0.append(meas_t,meas_x_s0)
            self._x_s1.append(meas_t,meas_x_s1)
            self._u_1.append(meas_t,meas_u_1)
            self._u_2.append(meas_t,meas_u_2)
            self._u_3.append(meas_t,meas_u_3)
            self._u_4.append(meas_t,meas_u_4)
            self._u_5.append(meas_t,meas_u_5)
            self._u_6.append(meas_t,meas_u_6)
            #self._c_1.append(meas_t,meas_c_1)
            #self._c_2.append(meas_t,meas_c_2)
            #self._v_1.append(meas_t,meas_v_1)
            #self._v_2.append(meas_t,meas_v_2)
            #self._p_c.append(meas_t,meas_p_c)



        if self.server_choice == _COLLECT_FB:
            cmd_fmt = "snmpwalk -c LTU -v 2c -Oqv 10.0.100.10 %s"

            mib_x = "LM-SENSORS-MIB::lmTempSensorsValue" #All core temp
            #mib_x_1 = "LM-SENSORS-MIB::lmTempSensorsValue.1" #Average temp socket 0 
            #mib_x_2 = "LM-SENSORS-MIB::lmTempSensorsValue.2" #Temp core 0
            #mib_x_3 = "LM-SENSORS-MIB::lmTempSensorsValue.3" #Temp core 1
            #mib_x_4 = "LM-SENSORS-MIB::lmTempSensorsValue.4" #Temp core 2
            #mib_x_5 = "LM-SENSORS-MIB::lmTempSensorsValue.5" #Temp core 3
            #mib_x_6 = "LM-SENSORS-MIB::lmTempSensorsValue.6" #Temp core 4
            #mib_x_7 = "LM-SENSORS-MIB::lmTempSensorsValue.7" #Temp core 5
            #mib_x_8 = "LM-SENSORS-MIB::lmTempSensorsValue.8" #Temp core 6
            #mib_x_9 = "LM-SENSORS-MIB::lmTempSensorsValue.9" #Temp core 7
            #mib_x_10 = "LM-SENSORS-MIB::lmTempSensorsValue.10" #Average temp socket 1
            #mib_x_11 = "LM-SENSORS-MIB::lmTempSensorsValue.11" #Temp core 0
            #mib_x_12 = "LM-SENSORS-MIB::lmTempSensorsValue.12" #Temp core 1
            #mib_x_13 = "LM-SENSORS-MIB::lmTempSensorsValue.13" #Temp core 2
            #mib_x_14 = "LM-SENSORS-MIB::lmTempSensorsValue.14" #Temp core 3
            #mib_x_15 = "LM-SENSORS-MIB::lmTempSensorsValue.15" #Temp core 4
            #mib_x_16 = "LM-SENSORS-MIB::lmTempSensorsValue.16" #Temp core 5
            #mib_x_17 = "LM-SENSORS-MIB::lmTempSensorsValue.17" #Temp core 6
            #mib_x_18 = "LM-SENSORS-MIB::lmTempSensorsValue.18" #Temp core 7

            mib_l = "HOST-RESOURCES-MIB::hrProcessorLoad" # All core temp 
            #mib_l_1 = "HOST-RESOURCES-MIB::hrProcessorLoad.196608" # core 0 
            #mib_l_2 = "HOST-RESOURCES-MIB::hrProcessorLoad.196609" # core 1
            #mib_l_3 = "HOST-RESOURCES-MIB::hrProcessorLoad.196610" # core 2
            #mib_l_4 = "HOST-RESOURCES-MIB::hrProcessorLoad.196611" # core 3
            #mib_l_5 = "HOST-RESOURCES-MIB::hrProcessorLoad.196612" # core 4
            #mib_l_6 = "HOST-RESOURCES-MIB::hrProcessorLoad.196613" # core 5
            #mib_l_7 = "HOST-RESOURCES-MIB::hrProcessorLoad.196614" # core 6
            #mib_l_8 = "HOST-RESOURCES-MIB::hrProcessorLoad.196615" # core 7
            #mib_l_9 = "HOST-RESOURCES-MIB::hrProcessorLoad.196616" # core 8
            #mib_l_10 = "HOST-RESOURCES-MIB::hrProcessorLoad.196617" # core 9
            #mib_l_11 = "HOST-RESOURCES-MIB::hrProcessorLoad.196618" # core 10
            #mib_l_12 = "HOST-RESOURCES-MIB::hrProcessorLoad.196619" # core 11
            #mib_l_13 = "HOST-RESOURCES-MIB::hrProcessorLoad.196620" # core 12
            #mib_l_14 = "HOST-RESOURCES-MIB::hrProcessorLoad.196621" # core 13
            #mib_l_15 = "HOST-RESOURCES-MIB::hrProcessorLoad.196622" # core 14
            #mib_l_16 = "HOST-RESOURCES-MIB::hrProcessorLoad.196623" # core 15
            #mib_l_17 = "HOST-RESOURCES-MIB::hrProcessorLoad.196624" # core 16
            #mib_l_18 = "HOST-RESOURCES-MIB::hrProcessorLoad.196625" # core 17
            #mib_l_19 = "HOST-RESOURCES-MIB::hrProcessorLoad.196626" # core 18
            #mib_l_20 = "HOST-RESOURCES-MIB::hrProcessorLoad.196627" # core 19
            #mib_l_21 = "HOST-RESOURCES-MIB::hrProcessorLoad.196628" # core 20
            #mib_l_22 = "HOST-RESOURCES-MIB::hrProcessorLoad.196629" # core 21
            #mib_l_23 = "HOST-RESOURCES-MIB::hrProcessorLoad.196630" # core 22
            #mib_l_24 = "HOST-RESOURCES-MIB::hrProcessorLoad.196631" # core 23
            #mib_l_25 = "HOST-RESOURCES-MIB::hrProcessorLoad.196632" # core 24
            #mib_l_26 = "HOST-RESOURCES-MIB::hrProcessorLoad.196633" # core 25
            #mib_l_27 = "HOST-RESOURCES-MIB::hrProcessorLoad.196634" # core 26
            #mib_l_28 = "HOST-RESOURCES-MIB::hrProcessorLoad.196635" # core 27
            #mib_l_29 = "HOST-RESOURCES-MIB::hrProcessorLoad.196636" # core 28
            #mib_l_30 = "HOST-RESOURCES-MIB::hrProcessorLoad.196637" # core 29
            #mib_l_31 = "HOST-RESOURCES-MIB::hrProcessorLoad.196638" # core 30
            #mib_l_32 = "HOST-RESOURCES-MIB::hrProcessorLoad.196639" # core 31

            #snmp_x = subprocess.check_output(cmd_fmt % mib_x, shell=True)
            p = subprocess.Popen(shlex.split(cmd_fmt % mib_x), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            snmp_x, err = p.communicate()

            #snmp_l = subprocess.check_output(cmd_fmt % mib_l, shell=True)
            p = subprocess.Popen(shlex.split(cmd_fmt % mib_l), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            snmp_l, err = p.communicate()

            #
            # Parse the outputs
            #
            def _parse_core_temperature(temp_str):
                # The temps are measured in tens of degrees Celsius
                return float(temp_str)/1000.

            def _parse_snmp_float(fs_str):
                # The fans are measured in RPM
                return float(fs_str)
            
            lines = snmp_x.splitlines()
            meas_x_0 = _parse_core_temperature(lines[0]) #Average temp socket 0
            meas_x_1 = _parse_core_temperature(lines[1]) #Temp core 0
            meas_x_2 = _parse_core_temperature(lines[2]) #Temp core 1
            meas_x_3 = _parse_core_temperature(lines[3]) #Temp core 2
            meas_x_4 = _parse_core_temperature(lines[4]) #Temp core 3
            meas_x_5 = _parse_core_temperature(lines[5]) #Temp core 4
            meas_x_6 = _parse_core_temperature(lines[6]) #Temp core 5
            meas_x_7 = _parse_core_temperature(lines[7]) #Temp core 6
            meas_x_8 = _parse_core_temperature(lines[8]) #Temp core 7
            meas_x_9 = _parse_core_temperature(lines[9]) #Average temp socket 1
            meas_x_10 = _parse_core_temperature(lines[10]) #Temp core 0
            meas_x_11 = _parse_core_temperature(lines[11]) #Temp core 1
            meas_x_12 = _parse_core_temperature(lines[12]) #Temp core 2
            meas_x_13 = _parse_core_temperature(lines[13]) #Temp core 3
            meas_x_14 = _parse_core_temperature(lines[14]) #Temp core 4
            meas_x_15 = _parse_core_temperature(lines[15]) #Temp core 5
            meas_x_16 = _parse_core_temperature(lines[16]) #Temp core 6
            meas_x_17 = _parse_core_temperature(lines[17]) #Temp core 7
        
            lines = snmp_l.splitlines()
            meas_l_0 = _parse_snmp_float(lines[0]) #Load core 0
            meas_l_1 = _parse_snmp_float(lines[1]) #Load core 1
            meas_l_2 = _parse_snmp_float(lines[2]) #Load core 2
            meas_l_3 = _parse_snmp_float(lines[3]) #Load core 3
            meas_l_4 = _parse_snmp_float(lines[4]) #Load core 4
            meas_l_5 = _parse_snmp_float(lines[5]) #Load core 5
            meas_l_6 = _parse_snmp_float(lines[6]) #Load core 6
            meas_l_7 = _parse_snmp_float(lines[7]) #Load core 7
            meas_l_8 = _parse_snmp_float(lines[8]) #Load core 8
            meas_l_9 = _parse_snmp_float(lines[9]) #Load core 9
            meas_l_10 = _parse_snmp_float(lines[10]) #Load core 10
            meas_l_11 = _parse_snmp_float(lines[11]) #Load core 11
            meas_l_12 = _parse_snmp_float(lines[12]) #Load core 12
            meas_l_13 = _parse_snmp_float(lines[13]) #Load core 13
            meas_l_14 = _parse_snmp_float(lines[14]) #Load core 14
            meas_l_15 = _parse_snmp_float(lines[15]) #Load core 15
            meas_l_16 = _parse_snmp_float(lines[16]) #Load core 16
            meas_l_17 = _parse_snmp_float(lines[17]) #Load core 17
            meas_l_18 = _parse_snmp_float(lines[18]) #Load core 18
            meas_l_19 = _parse_snmp_float(lines[19]) #Load core 19
            meas_l_20 = _parse_snmp_float(lines[20]) #Load core 20
            meas_l_21 = _parse_snmp_float(lines[21]) #Load core 21
            meas_l_22 = _parse_snmp_float(lines[22]) #Load core 22
            meas_l_23 = _parse_snmp_float(lines[23]) #Load core 23
            meas_l_24 = _parse_snmp_float(lines[24]) #Load core 24
            meas_l_25 = _parse_snmp_float(lines[25]) #Load core 25
            meas_l_26 = _parse_snmp_float(lines[26]) #Load core 26
            meas_l_27 = _parse_snmp_float(lines[27]) #Load core 27
            meas_l_28 = _parse_snmp_float(lines[28]) #Load core 28
            meas_l_29 = _parse_snmp_float(lines[29]) #Load core 29
            meas_l_30 = _parse_snmp_float(lines[30]) #Load core 30
            meas_l_31 = _parse_snmp_float(lines[31]) #Load core 31

            self._x_0.append(meas_t, meas_x_0)
            self._x_1.append(meas_t, meas_x_1)
            self._x_2.append(meas_t, meas_x_2)
            self._x_3.append(meas_t, meas_x_3)
            self._x_4.append(meas_t, meas_x_4)
            self._x_5.append(meas_t, meas_x_5)
            self._x_6.append(meas_t, meas_x_6)
            self._x_7.append(meas_t, meas_x_7)
            self._x_8.append(meas_t, meas_x_8)
            self._x_9.append(meas_t, meas_x_9)
            self._x_10.append(meas_t, meas_x_10)
            self._x_11.append(meas_t, meas_x_11)
            self._x_12.append(meas_t, meas_x_12)
            self._x_13.append(meas_t, meas_x_13)
            self._x_14.append(meas_t, meas_x_14)
            self._x_15.append(meas_t, meas_x_15)
            self._x_16.append(meas_t, meas_x_16)
            self._x_17.append(meas_t, meas_x_17)

            self._l_0.append(meas_t, meas_l_0)
            self._l_1.append(meas_t, meas_l_1)
            self._l_2.append(meas_t, meas_l_2)
            self._l_3.append(meas_t, meas_l_3)
            self._l_4.append(meas_t, meas_l_4)
            self._l_5.append(meas_t, meas_l_5)
            self._l_6.append(meas_t, meas_l_6)
            self._l_7.append(meas_t, meas_l_7)
            self._l_8.append(meas_t, meas_l_8)
            self._l_9.append(meas_t, meas_l_9)
            self._l_10.append(meas_t, meas_l_10)
            self._l_11.append(meas_t, meas_l_11)
            self._l_12.append(meas_t, meas_l_12)
            self._l_13.append(meas_t, meas_l_13)
            self._l_14.append(meas_t, meas_l_14)
            self._l_15.append(meas_t, meas_l_15)
            self._l_16.append(meas_t, meas_l_16)
            self._l_17.append(meas_t, meas_l_17)
            self._l_18.append(meas_t, meas_l_18)
            self._l_19.append(meas_t, meas_l_19)
            self._l_20.append(meas_t, meas_l_20)
            self._l_21.append(meas_t, meas_l_21)
            self._l_22.append(meas_t, meas_l_22)
            self._l_23.append(meas_t, meas_l_23)
            self._l_24.append(meas_t, meas_l_24)
            self._l_25.append(meas_t, meas_l_25)
            self._l_26.append(meas_t, meas_l_26)
            self._l_27.append(meas_t, meas_l_27)
            self._l_28.append(meas_t, meas_l_28)
            self._l_29.append(meas_t, meas_l_29)
            self._l_30.append(meas_t, meas_l_30)
            self._l_31.append(meas_t, meas_l_31)


    def fetch_use_ipmi(self, meas_t):
        assert isinstance(meas_t, float)
        #
        # issue the ipmi query
        #
        # ! todo: explain the command arguments
        #
        if self.server_choice == _COLLECT_DELL:
            cmd = "ipmitool -c -I lanplus -U ltu -P LTU123 -H 192.168.21.151 sdr list full"
            p = subprocess.Popen(shlex.split(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            ipmi_all, err = p.communicate()

            count = 0
            lines = ipmi_all.splitlines()
            for l in lines:
                match = re.match("Fan1\sRPM,(\d+),RPM,ok", l)
                if match is not None:
                    self._u_1.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Fan2\sRPM,(\d+),RPM,ok", l)
                if match is not None:
                    self._u_2.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Fan3\sRPM,(\d+),RPM,ok", l)
                if match is not None:
                    self._u_3.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Fan4\sRPM,(\d+),RPM,ok", l)
                if match is not None:
                    self._u_4.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Fan5\sRPM,(\d+),RPM,ok", l)
                if match is not None:
                    self._u_5.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Fan6\sRPM,(\d+),RPM,ok", l)
                if match is not None:
                    self._u_6.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Inlet\sTemp,(\d+),degrees\sC,ok", l)
                if match is not None:
                    self._x_i.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("CPU\sUsage,(\d+),percent,ok", l)
                if match is not None:
                    self._l_c.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("IO\sUsage,(\d+),percent,ok", l)
                if match is not None:
                    self._l_io.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("MEM\sUsage,(\d+),percent,ok", l)
                if match is not None:
                    self._l_m.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("SYS\sUsage,(\d+),percent,ok", l)
                if match is not None:
                    self._l_s.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Exhaust\sTemp,(\d+),degrees\sC,ok", l)
                if match is not None:
                    self._x_o.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Temp,(\d+),degrees\sC,ok", l)
                if match is not None:
                    if count == 0:
                        self._x_s0.append(meas_t, float(match.group(1)))
                        count +=1
                    else:
                        self._x_s1.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Current\s1,([\d\.]+),Amps,ok", l)
                if match is not None:
                    self._c_1.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Current\s2,([\d\.]+),Amps,ok", l)
                if match is not None:
                    self._c_2.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Voltage\s1,(\d+),Volts,ok", l)
                if match is not None:
                    self._v_1.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Voltage\s2,(\d+),Volts,ok", l)
                if match is not None:
                    self._v_2.append(meas_t, float(match.group(1)))
                    continue
                match = re.match("Pwr\sConsumption,(\d+),Watts,ok", l)
                if match is not None:
                    self._p_c.append(meas_t, float(match.group(1)))
                    continue

        elif self.server_choice == _COLLECT_FB:
	    cmd = "ipmi-sensors -t Temperature -t Fan --comma-separated-output --ignore-not-available-sensors --no-sensor-type-output --no-header-output -u sics -p sics -D LAN_2_0 -h 10.0.100.122"
            p = subprocess.Popen(shlex.split(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            ipmi_all, err = p.communicate()
            lines = ipmi_all.splitlines()
            for l in lines:
                #257,Outlet Cntr Temp,21.00,C,'OK'
                match = re.match("\d+,Outlet\sCntr\sTemp\s*,([+-]?\d+(?:\.\d+)?),C,'OK'", l)
                if match is not None:
                    self._x_o.append(meas_t, float(match.group(1)))
                    continue
                #263,Inlet Temp      ,21.00,C,'OK'
                match = re.match("\d+,Inlet\sTemp\s*,([+-]?\d+(?:\.\d+)?),C,'OK'", l)
                if match is not None:
                    self._x_i.append(meas_t, float(match.group(1)))
                    continue
                #265,P0 Therm Margin ,-68.00,C,'OK'
                match = re.match("\d+,P0\sTherm\sMargin\s*,([+-]?\d+(?:\.\d+)?),C,'OK'", l)
                if match is not None:
                    self._x_s0.append(meas_t, float(match.group(1)))
                    continue
                #266,P1 Therm Margin ,-69.00,C,'OK'
                match = re.match("\d+,P1\sTherm\sMargin\s*,([+-]?\d+(?:\.\d+)?),C,'OK'", l)
                if match is not None:
                    self._x_s1.append(meas_t, float(match.group(1)))
                    continue
                #273,P0 DIMM Temp    ,22.00,C,'OK'
                match = re.match("\d+,P0\sDIMM\sTemp\s*,([+-]?\d+(?:\.\d+)?),C,'OK'", l)
                if match is not None:
                    self._x_d0.append(meas_t, float(match.group(1)))
                    continue
                #274,P1 DIMM Temp    ,21.00,C,'OK'
                match = re.match("\d+,P1\sDIMM\sTemp\s*,([+-]?\d+(?:\.\d+)?),C,'OK'", l)
                if match is not None:
                    self._x_d1.append(meas_t, float(match.group(1)))
                    continue
                #326,SYS_Fan0        ,2475.00,RPM,'OK'
                match = re.match("\d+,SYS_Fan0\s*,([+-]?\d+(?:\.\d+)?),RPM,'OK'", l)
                if match is not None:
                    self._u_1.append(meas_t, float(match.group(1)))
                    continue
                #327,SYS_Fan1        ,2475.00,RPM,'OK'
                match = re.match("\d+,SYS_Fan1\s*,([+-]?\d+(?:\.\d+)?),RPM,'OK'", l)
                if match is not None:
                    self._u_2.append(meas_t, float(match.group(1)))
                    continue

    def collect(self, sampling_period, timelength):
        assert isinstance(sampling_period, (int,float))
        assert sampling_period >= 1/_MAX_SAMPLING_PERIOD
        assert timelength > 0
        assert isinstance(timelength, (int,float))

        zero_time_ipmi = None
        zero_time_snmp = None
        zero_time = None
        zero_pwr = None
        endtest_time = timelength * 3600
        print "Endtest time %d [sec]" % endtest_time
        
        late_counter = 0
        loop_counter = 0
        while True:
            loop_counter = loop_counter + 1
            cur_time = time.time()
            if zero_time == None:
                zero_time = cur_time
            meas_t = cur_time - zero_time
            if meas_t >= endtest_time:
                print "Reached end of test: %.2f / %.2f [sec]" % (meas_t, endtest_time)
                break

            if self._use_ipmi:
                cur_time = time.time()
                if zero_time_ipmi == None:
                    zero_time_ipmi = cur_time
                    self._s_t_ipmi.save_start_time(zero_time_ipmi)
                meas_t_ipmi = cur_time - zero_time_ipmi
                self.fetch_use_ipmi(meas_t_ipmi)

            if self._use_snmp:
                cur_time = time.time()
                if zero_time_snmp == None:
                    zero_time_snmp = cur_time
                    self._s_t_snmp.save_start_time(zero_time_snmp)
                meas_t_snmp = cur_time - zero_time_snmp
                self.fetch_snmp(meas_t_snmp, zero_pwr)
           
            if self.conn:
                self._relay_data(meas_t_ipmi, meas_t_snmp)
            
            # wait until the next sampling time
            delta_interval = time.time() - cur_time

            if not sampling_period - delta_interval <= 0:
                time.sleep(sampling_period - delta_interval)
            else:
                late_counter = late_counter + 1
                print " ! late %.3fs rate=%.2f" % (delta_interval - sampling_period, late_counter/float(loop_counter))

    def save_numpy(self,path):
        x_i_time, x_i_data = self._x_i.get_time_with_data()
        x_o_time, x_o_data = self._x_o.get_time_with_data()
        x_s0_time,x_s0_data = self._x_s0.get_time_with_data()
        x_s1_time,x_s1_data = self._x_s1.get_time_with_data()
        u_1_time, u_1_data = self._u_1.get_time_with_data()
        u_2_time, u_2_data = self._u_2.get_time_with_data()
        u_3_time, u_3_data = self._u_3.get_time_with_data()
        u_4_time, u_4_data = self._u_4.get_time_with_data()
        u_5_time, u_5_data = self._u_5.get_time_with_data()
        u_6_time, u_6_data = self._u_6.get_time_with_data()
        l_c_time, l_c_data = self._l_c.get_time_with_data()
        l_io_time,l_io_data = self._l_io.get_time_with_data()
        l_m_time, l_m_data = self._l_m.get_time_with_data()
        l_s_time, l_s_data = self._l_s.get_time_with_data()
        v_1_time, v_1_data = self._v_1.get_time_with_data()
        v_2_time, v_2_data = self._v_2.get_time_with_data()
        c_1_time, c_1_data = self._c_1.get_time_with_data()
        c_2_time, c_2_data = self._c_2.get_time_with_data()
        p_c_time, p_c_data = self._p_c.get_time_with_data()
        
        if not path.endswith(".npz"):
            path = path + ".npz"
        numpy.savez(path, x_i_t = x_i_time, x_i = x_i_data, \
            x_o_t = x_o_time, x_o = x_o_data, \
            x_s0_t = x_s0_time, x_s0 = x_s0_data, \
            x_s1_t = x_s1_time, x_s1 = x_s1_data, \
            u_1_t = u_1_time, u_1 = u_1_data, \
            u_2_t = u_2_time, u_2 = u_2_data, \
            u_3_t = u_3_time, u_3 = u_3_data, \
            u_4_t = u_4_time, u_4 = u_4_data, \
            u_5_t = u_5_time, u_5 = u_5_data, \
            u_6_t = u_6_time, u_6 = u_6_data, \
            l_c_t = l_c_time, l_c = l_c_data, \
            l_io_t = l_io_time, l_io = l_io_data, \
            l_m_t = l_m_time, l_m = l_m_data, \
            l_s_t = l_s_time, l_s = l_s_data, \
            v_1_t = v_1_time, v_1 = v_1_data, \
            v_2_t = v_2_time, v_2 = v_2_data, \
            c_1_t = c_1_time, c_1 = c_1_data, \
            c_2_t = c_2_time, c_2 = c_2_data, \
            p_c_t = p_c_time, p_c = p_c_data)
        

    def save_matlab(self, path, period, timelength):

        # IPMI
        x_i_time, x_i_data = self._x_i.get_time_with_data()
        x_o_time, x_o_data = self._x_o.get_time_with_data()
        x_s0_time, x_s0_data = self._x_s0.get_time_with_data()
        x_s1_time, x_s1_data = self._x_s1.get_time_with_data()
        x_d0_time, x_d0_data = self._x_d0.get_time_with_data()
        x_d1_time, x_d1_data = self._x_d1.get_time_with_data()
        u_1_time, u_1_data = self._u_1.get_time_with_data()
        u_2_time, u_2_data = self._u_2.get_time_with_data()
        u_3_time, u_3_data = self._u_3.get_time_with_data()
        u_4_time, u_4_data = self._u_4.get_time_with_data()
        u_5_time, u_5_data = self._u_5.get_time_with_data()
        u_6_time, u_6_data = self._u_6.get_time_with_data()
        l_c_time, l_c_data = self._l_c.get_time_with_data()
        l_io_time, l_io_data = self._l_io.get_time_with_data()
        l_m_time, l_m_data = self._l_m.get_time_with_data()
        l_s_time, l_s_data = self._l_s.get_time_with_data()
        v_1_time, v_1_data = self._v_1.get_time_with_data()
        v_2_time, v_2_data = self._v_2.get_time_with_data()
        c_1_time, c_1_data = self._c_1.get_time_with_data()
        c_2_time, c_2_data = self._c_2.get_time_with_data()
        p_c_time, p_c_data = self._p_c.get_time_with_data()

        # SNMP
        x_0_time, x_0_data = self._x_0.get_time_with_data()
        x_1_time, x_1_data = self._x_1.get_time_with_data()
        x_2_time, x_2_data = self._x_2.get_time_with_data()
        x_3_time, x_3_data = self._x_3.get_time_with_data()
        x_4_time, x_4_data = self._x_4.get_time_with_data()
        x_5_time, x_5_data = self._x_5.get_time_with_data()
        x_6_time, x_6_data = self._x_6.get_time_with_data()
        x_7_time, x_7_data = self._x_7.get_time_with_data()
        x_8_time, x_8_data = self._x_8.get_time_with_data()
        x_9_time, x_9_data = self._x_9.get_time_with_data()
        x_10_time, x_10_data = self._x_10.get_time_with_data()
        x_11_time, x_11_data = self._x_11.get_time_with_data()
        x_12_time, x_12_data = self._x_12.get_time_with_data()
        x_13_time, x_13_data = self._x_13.get_time_with_data()
        x_14_time, x_14_data = self._x_14.get_time_with_data()
        x_15_time, x_15_data = self._x_15.get_time_with_data()
        x_16_time, x_16_data = self._x_16.get_time_with_data()
        x_17_time, x_17_data = self._x_17.get_time_with_data()

        l_0_time, l_0_data = self._l_0.get_time_with_data()
        l_1_time, l_1_data = self._l_1.get_time_with_data()
        l_2_time, l_2_data = self._l_2.get_time_with_data()
        l_3_time, l_3_data = self._l_3.get_time_with_data()
        l_4_time, l_4_data = self._l_4.get_time_with_data()
        l_5_time, l_5_data = self._l_5.get_time_with_data()
        l_6_time, l_6_data = self._l_6.get_time_with_data()
        l_7_time, l_7_data = self._l_7.get_time_with_data()
        l_8_time, l_8_data = self._l_8.get_time_with_data()
        l_9_time, l_9_data = self._l_9.get_time_with_data()
        l_10_time, l_10_data = self._l_10.get_time_with_data()
        l_11_time, l_11_data = self._l_11.get_time_with_data()
        l_12_time, l_12_data = self._l_12.get_time_with_data()
        l_13_time, l_13_data = self._l_13.get_time_with_data()
        l_14_time, l_14_data = self._l_14.get_time_with_data()
        l_15_time, l_15_data = self._l_15.get_time_with_data()
        l_16_time, l_16_data = self._l_16.get_time_with_data()
        l_17_time, l_17_data = self._l_17.get_time_with_data()
        l_18_time, l_18_data = self._l_18.get_time_with_data()
        l_19_time, l_19_data = self._l_19.get_time_with_data()
        l_20_time, l_20_data = self._l_20.get_time_with_data()
        l_21_time, l_21_data = self._l_21.get_time_with_data()
        l_22_time, l_22_data = self._l_22.get_time_with_data()
        l_23_time, l_23_data = self._l_23.get_time_with_data()
        l_24_time, l_24_data = self._l_24.get_time_with_data()
        l_25_time, l_25_data = self._l_25.get_time_with_data()
        l_26_time, l_26_data = self._l_26.get_time_with_data()
        l_27_time, l_27_data = self._l_27.get_time_with_data()
        l_28_time, l_28_data = self._l_28.get_time_with_data()
        l_29_time, l_29_data = self._l_29.get_time_with_data()
        l_30_time, l_30_data = self._l_30.get_time_with_data()
        l_31_time, l_31_data = self._l_31.get_time_with_data()

        start_time_ipmi = self._s_t_ipmi.get_start_time()
        start_time_snmp = self._s_t_snmp.get_start_time()
        
        if not path.endswith(".mat"):
             path = path + ".mat"

        scipy.io.savemat(path, {'timelength':timelength, 'period':period, \
                    's_t_ipmi':start_time_ipmi, 's_t_snmp':start_time_snmp, \
                    'x_0':x_0_data,   'x_0_t':x_0_time, \
                    'x_1':x_1_data,   'x_1_t':x_1_time, \
                    'x_2':x_2_data,   'x_2_t':x_2_time, \
                    'x_3':x_3_data,   'x_3_t':x_3_time, \
                    'x_4':x_4_data,   'x_4_t':x_4_time, \
                    'x_5':x_5_data,   'x_5_t':x_5_time, \
                    'x_6':x_6_data,   'x_6_t':x_6_time, \
                    'x_7':x_7_data,   'x_7_t':x_7_time, \
                    'x_8':x_8_data,   'x_8_t':x_8_time, \
                    'x_9':x_9_data,   'x_9_t':x_9_time, \
                    'x_10':x_10_data, 'x_10_t':x_10_time, \
                    'x_11':x_11_data, 'x_11_t':x_11_time,\
                    'x_12':x_12_data, 'x_12_t':x_12_time, \
                    'x_13':x_13_data, 'x_13_t':x_13_time, \
                    'x_14':x_14_data, 'x_14_t':x_14_time, \
                    'x_15':x_15_data, 'x_15_t':x_15_time, \
                    'x_16':x_16_data, 'x_16_t':x_16_time, \
                    'x_17':x_17_data, 'x_17_t':x_17_time, \
                    'l_0':l_0_data,   'l_0_t':l_0_time, \
                    'l_1':l_1_data,   'l_1_t':l_1_time, \
                    'l_2':l_2_data,   'l_2_t':l_2_time, \
                    'l_3':l_3_data,   'l_3_t':l_3_time, \
                    'l_4':l_4_data,   'l_4_t':l_4_time, \
                    'l_5':l_5_data,   'l_5_t':l_5_time, \
                    'l_6':l_6_data,   'l_6_t':l_6_time, \
                    'l_7':l_7_data,   'l_7_t':l_7_time, \
                    'l_8':l_8_data,   'l_8_t':l_8_time, \
                    'l_9':l_9_data,   'l_9_t':l_9_time, \
                    'l_10':l_10_data, 'l_10_t':l_10_time, \
                    'l_11':l_11_data, 'l_11_t':l_11_time,\
                    'l_12':l_12_data, 'l_12_t':l_12_time, \
                    'l_13':l_13_data, 'l_13_t':l_13_time, \
                    'l_14':l_14_data, 'l_14_t':l_14_time, \
                    'l_15':l_15_data, 'l_15_t':l_15_time, \
                    'l_16':l_16_data, 'l_16_t':l_16_time, \
                    'l_17':l_17_data, 'l_17_t':l_17_time, \
                    'l_18':l_18_data, 'l_18_t':l_18_time, \
                    'l_19':l_19_data, 'l_19_t':l_19_time, \
                    'l_20':l_20_data, 'l_20_t':l_20_time, \
                    'l_21':l_21_data, 'l_21_t':l_21_time, \
                    'l_22':l_22_data, 'l_22_t':l_22_time, \
                    'l_23':l_23_data, 'l_23_t':l_23_time, \
                    'l_24':l_24_data, 'l_24_t':l_24_time, \
                    'l_25':l_25_data, 'l_25_t':l_25_time, \
                    'l_26':l_26_data, 'l_26_t':l_26_time, \
                    'l_27':l_27_data, 'l_27_t':l_27_time, \
                    'l_28':l_28_data, 'l_28_t':l_28_time, \
                    'l_29':l_29_data, 'l_29_t':l_29_time, \
                    'l_30':l_30_data, 'l_30_t':l_30_time,\
                    'l_31':l_31_data, 'l_31_t':l_31_time, \
                    'x_i':x_i_data,   'x_i_t':x_i_time, \
                    'x_o':x_o_data,   'x_o_t':x_o_time, \
                    'x_s0':x_s0_data, 'x_s0_t':x_s0_time, \
                    'x_s1':x_s1_data, 'x_s1_t':x_s1_time, \
                    'x_d0':x_d0_data, 'x_d0_t':x_d0_time, \
                    'x_d1':x_d1_data, 'x_d1_t':x_d1_time, \
                    'u_1':u_1_data,   'u_1_t':u_1_time, \
                    'u_2':u_2_data,   'u_2_t':u_2_time, \
                    'u_3':u_3_data,   'u_3_t':u_3_time, \
                    'u_4':u_4_data,   'u_4_t':u_4_time, \
                    'u_5':u_5_data,   'u_5_t':u_5_time, \
                    'u_6':u_6_data,   'u_6_t':u_6_time, \
                    'l_c':l_c_data,   'l_c_t':l_c_time, \
                    'l_io':l_io_data, 'l_io_t':l_io_time,\
                    'l_m':l_m_data,   'l_m_t':l_m_time, \
                    'l_s':l_s_data,   'l_s_t':l_s_time, \
                    'c_1':c_1_data,   'c_1_t':c_1_time, \
                    'c_2':c_2_data,   'c_2_t':c_2_time, \
                    'v_1':v_1_data,   'v_1_t':v_1_time, \
                    'v_2':v_2_data,   'v_2_t':v_2_time, \
                    'p_c':p_c_data,   'p_c_t':p_c_time, })

    def _relay_data(self, meas_t_ipmi, meas_t_snmp):
        if self.conn:
            msg = 'SNMP:' + 'x_t_snmp,' + str(meas_t_snmp) + ',s_t_snmp,' + str(self._s_t_snmp.get_start_time()) + \
                ','+ self._x_0.get_name() +',' + str(self._x_0.get_last_value()) + ',x_1,' + str(self._x_1.get_last_value()) + \
                ',x_2,' + str(self._x_2.get_last_value()) + ',x_3,' + str(self._x_3.get_last_value()) + \
                ',x_4,' + str(self._x_4.get_last_value()) + ',x_5,' + str(self._x_5.get_last_value()) + \
                ',x_6,' + str(self._x_6.get_last_value()) + ',x_7,' + str(self._x_7.get_last_value()) + \
                ',x_8,' + str(self._x_8.get_last_value()) + ',x_9,' + str(self._x_9.get_last_value()) + \
                ',x_10,' + str(self._x_10.get_last_value()) + ',x_11,' + str(self._x_11.get_last_value()) + \
                ',x_12,' + str(self._x_12.get_last_value()) + ',x_13,' + str(self._x_13.get_last_value()) + \
                ',x_14,' + str(self._x_14.get_last_value()) + ',x_15,' + str(self._x_15.get_last_value()) + \
                ',x_16,' + str(self._x_16.get_last_value()) + ',x_17,' + str(self._x_17.get_last_value()) + '\n' + \
                ',l_0,' + str(self._l_0.get_last_value()) + ',l_1,' + str(self._l_1.get_last_value()) + \
                ',l_2,' + str(self._l_2.get_last_value()) + ',l_3,' + str(self._l_3.get_last_value()) + \
                ',l_4,' + str(self._l_4.get_last_value()) + ',l_5,' + str(self._l_5.get_last_value()) + \
                ',l_6,' + str(self._l_6.get_last_value()) + ',l_7,' + str(self._l_7.get_last_value()) + \
                ',l_8,' + str(self._l_8.get_last_value()) + ',l_9,' + str(self._l_9.get_last_value()) + \
                ',l_10,' + str(self._l_10.get_last_value()) + ',l_11,' + str(self._l_11.get_last_value()) + \
                ',l_12,' + str(self._l_12.get_last_value()) + ',l_13,' + str(self._l_13.get_last_value()) + \
                ',l_14,' + str(self._l_14.get_last_value()) + ',l_15,' + str(self._l_15.get_last_value()) + \
                ',l_16,' + str(self._l_16.get_last_value()) + ',l_17,' + str(self._l_17.get_last_value()) + \
                ',l_18,' + str(self._l_18.get_last_value()) + ',l_19,' + str(self._l_19.get_last_value()) + \
                ',l_20,' + str(self._l_20.get_last_value()) + ',l_21,' + str(self._l_21.get_last_value()) + \
                ',l_22,' + str(self._l_22.get_last_value()) + ',l_23,' + str(self._l_23.get_last_value()) + \
                ',l_24,' + str(self._l_24.get_last_value()) + ',l_25,' + str(self._l_25.get_last_value()) + \
                ',l_26,' + str(self._l_26.get_last_value()) + ',l_27,' + str(self._l_27.get_last_value()) + \
                ',l_28,' + str(self._l_28.get_last_value()) + ',l_29,' + str(self._l_29.get_last_value()) + \
                ',l_30,' + str(self._l_30.get_last_value()) + ',l_31,' + str(self._l_31.get_last_value()) + '\n' + \
                'IPMI:' +  'x_t_ipmi,' + str(meas_t_ipmi) + \
                ',s_t_ipmi,' + str(self._s_t_ipmi.get_start_time()) + ',x_i,' + str(self._x_i.get_last_value()) + \
                ',x_o,' + str(self._x_0.get_last_value()) + ',x_s0,' + str(self._x_s0.get_last_value()) + \
                ',x_s1,' + str(self._x_s1.get_last_value()) + ',x_d0,' + str(self._x_d0.get_last_value()) + \
                ',x_d1,' + str(self._x_d1.get_last_value()) + ',u_1,' + str(self._u_1.get_last_value()) + \
                ',u_2,' + str(self._u_2.get_last_value()) + ',u_3,' + str(self._u_3.get_last_value()) + \
                ',u_4,' + str(self._u_4.get_last_value()) + ',u_5,' + str(self._u_5.get_last_value()) + \
                ',u_6,' + str(self._u_6.get_last_value()) + ',l_c,' + str(self._l_c.get_last_value()) + \
                ',l_io,' + str(self._l_io.get_last_value()) + ',l_m,' + str(self._l_m.get_last_value()) + \
                ',l_s,' + str(self._l_s.get_last_value()) + ',c_1,' + str(self._c_1.get_last_value()) + \
                ',c_2,' + str(self._c_2.get_last_value()) + ',v_1,' + str(self._v_1.get_last_value()) + \
                ',v_2,' + str(self._v_2.get_last_value()) + ',p_c,' + str(self._p_c.get_last_value()) + '\n'

            conn.send(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--relay", default=False, action='store_true', help="Stream the data continuously to connected client")
    parser.add_argument("-t","--timelength", dest="timelength", default=1, help="The runtime of the script (default 1h)")
    parser.add_argument("-i","--ipmi", dest='use_ipmi', default=False, action='store_true', help="Use IPMI")
    parser.add_argument("-s","--snmp", dest='use_snmp', default=False, action='store_true', help="Use SNMP")
    parser.add_argument("-fb","--facebook", default=False, action='store_true', help="Collect from Facebook server insted of Dell")
    parser.add_argument("-T","--preiod", dest="period", default=1, help="The sampling period in seconds (default 1s)")
    parser.add_argument("-o","--outfile", dest="outfile", default=None, help="Path to the output file (numpy .npz format)")
    parser.add_argument("-m","--outfile-matlab", dest="outfile_mat", default=None, help="Path to the output file (matlab .mat format)")
    
    args = parser.parse_args()

    try:
        period = float(args.period)
    except:
        print "The sampling period \"%s\" is not a numeric type" % args.period
        sys.exit(1)
    try:
        timelength = float(args.timelength)
    except:
        print "The timelength \"%s\" is not a numeric type" % args.timelength
        sys.exit(1)

    if args.facebook:
        server_choice = _COLLECT_FB
    else:
        server_choice = _COLLECT_DELL

    conn=None
    if args.relay:
        #server_address = './server_monitor_socket'
        #try:
        #    os.unlink(server_address)
        #except OSError:
        #    if os.path.exists(server_address):
        #        raise
        #s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        #s.bind(server_address)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(_TCP_IP, _TCP_PORT)
        s.listen(1)
        print "Waiting for a client to connect ..."
        conn, addr = s.accept()
        print "... got a connection: " + addr[0] + ':' + addr[1]

    server = server(args.use_ipmi, args.use_snmp, server_choice, conn)
    server.collect(period, timelength)

    if args.outfile is not None:
        server.save_numpy(args.outfile)
            
    if args.outfile_mat is not None:
        if args.use_ipmi or args.use_snmp:
            server.save_matlab(args.outfile_mat, period, timelength)
    
    sys.exit(0)
