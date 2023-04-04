#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 16:07:08 2022

@author: vaughn
"""

"""
- Create Device Name get code
        (BORO is working on this) 

- finish this data structure

- Create functions code (Main) 

- GLOBAL VARIABLES
    - int temp low
    - string device name  ( locateed in base_dir) 
    - int run
    
    
base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_folder1 = glob.glob(base_dir + '28*')[1]
device_folder2 = glob.glob(base_dir + '28*')[2]
device_folder3 = glob.glob(base_dir + '28*')[3]
device_folder4 = glob.glob(base_dir + '28*')[4]
device_folder5 = glob.glob(base_dir + '28*')[5]
device_folder6 = glob.glob(base_dir + '28*')[6]
device_folder7 = glob.glob(base_dir + '28*')[7]
device_folder8 = glob.glob(base_dir + '28*')[8]

!!! Need to rework this into a novel function for collecting and assigning all unique
sensor_Ids to pass them each to an array of unique Temp_Zone class instances    
    
!!! DART/FLUTTER Control Requirements need to be implemented !!!

"""
import time
import Rpi.GPIO as GPIO

"""
!!! Look at updateing the inputs required to generate a zone..... 
    see if sensor_ID + device can be replaced by the full sys/bus '28*' pulled directly from the device folder
"""
class Temp_zone: 
    def __init__(self, sensor_ID, device,  gpio_signal_pin, low_temp_value):
        '''
        !!! This one may need to be updated based upon how we gather all the sensor_IDs
        from the root directory
        
        create a function outside of this file to gather them all  and use it pass sensor_IDs
        for each class instance within an array

        Parameters
        ----------
        sensor_ID : int
            sensor ID gotten from the root directory
            
        device : string
            device root directory
            
        GPIO_pin : int
            assigned GPIO to process zone heating activation requirements
            
        low_temp_value : int
            Global variable input from user to establish lowest viable temperature

        Returns
        -------
        None.

        '''
        
        self.sensor_ID = sensor_ID                              # 28-bit sensor ID value for direct assignment
        self.device = device                                    # root directory of sensors
        self.gpio_signal_pin = gpio_signal_pin                  # dedicated GPIO output pin -> to relay
        self.current_temp = 0                                   # initialized to 0, updates on get_temp()
        self.temp_logs = {
                            }                                    # stores get_temp() value : current_time
        
        self.threshold = low_temp_value + ( 0.075 * low_temp_value)  # creates a 7.5% buffer above the minumum threshold 
                                                                     # This ensures heaters wont shut off at low_temp_value zone beyond 
                                                                     # !!!!! x =-y^{3} + 120
                                                                     # Rework this algebra so that lower low_temp_values have higher temp
                                        
        self.threshold_flag = False                                     # Flags if out of temperature bound and activates 
                                                                        # GPIO output pin 
                                                                        #
                                                                        # Initialize all to False prior to first iteration

                                    
                        
                                    
    def temp_check(self):
        '''
        Comparees current temperature against minimu threshold
        
        Updates threshold flag to turn on our of
        
        
        '''
        if self.current_temp <= self.threshold:
            self.threshold_flag = True
        
        elif self.current_temp > self.threshold:
            self.threshold_flag = False
        
        
        
        
        
    def gpio_pin_output(self):
        '''
        Sends signal to dedicated GPIO_pin, to activate relay allowing heater assigned to 
        this thermal zone to turn on. 
        Otherwise if zone is within tolerance & activated, the zone will be turned off

        Returns
        -------
        None.

        '''
        
        GPIO.output(self.gpio_signal_pin, self.threshold_flag)
        
        
    def get_temp(self): 
        
        '''
        R
        
        '''
        
        raw_temp = self.device + self.sensor_ID + '/w1_slave'
        f = open(raw_temp, 'r')
        lines = f.readlines()
        f.close()
        
        equals_pos = lines[1].find('t=')
       
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        
        self.current_temp = temp_f
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        self.temp_logs[current_time] = self.current_temp
        
        
        
        return self.current_temp
        
        
        
