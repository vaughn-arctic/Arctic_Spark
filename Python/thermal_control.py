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
  
"""
import time
import glob
import os
import Rpi.GPIO as GPIO

sensor_locations = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')
sensor_array = []
temp_zone_lows = []


"""
!!! Look at updateing the inputs required to generate a zone..... 
    see if sensor_ID + device can be replaced by the full sys/bus '28*' pulled directly from the device folder
"""


# 1. Create sensor pin arrea

GPIO.setmode(GPIO.Board)
GPIO.setwarnings(False)
gpio_pin_array = [ 22, 29, 31, 32, 35, 36, 37, 38]   # dedicated out-put pins available on raspberry pi 

'''
                                Still working on the spatial requirments of this. 
                                Currently an 8 zone model (2 x 2 x 2 zones [18" x 18" x 18"] ) 
                                Consideration given to allowing user multi-modes (8 zone v. 16 zone) 
                                Include all GPIO pins and account for Temp_zone creation based upon 
                                combining multiple zones / sensors into a single class instance
                                Methods from the class are echoed to all hardware attached


'''


# get sensor_lsit
# itterate sensor list 

# for 
class Temp_zone: 
    def __init__(self, sensor_ID, gpio_signal_pin, low_temp_value):
        '''
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
        
        self.sensor_ID = sensor_ID                                      # 28-bit sensor ID + 
        self.gpio_signal_pin = gpio_signal_pin                          # dedicated GPIO output pin -> to relay
        self.current_temp = 0                                           # initialized to 0, updates on get_temp()
        self.temp_logs = { }                                           # stores get_temp() value : current_time
        
        self.threshold = low_temp_value + ( 0.125 * low_temp_value)  # creates a 7.5% buffer above the minumum threshold 
                                                                     # This ensures heaters wont shut off at low_temp_value zone beyond 
                                                                     # !!!!! x =-y^{3} + 120
                                                                     # Rework this algebra so that lower low_temp_values have higher temp thresholds
                                        
        self.threshold_flag = False                                     # Flags if out of temperature bound and activates 
                                                                        # GPIO output pin 
                                                                        #
                                                                        # Initialize all to False prior to first iteration            
                                    
    def temp_check(self):
        '''
        Comparees current temperature against minimu threshold
        Updates threshold flag to turn on our off
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

        '''
       
        GPIO.output(self.gpio_signal_pin, self.threshold_flag)
        
        
    def get_temp(self): 

        f = open(self.sensor_ID, 'r')  # read in current data from dedicated sensor
        lines = f.readlines()
        f.close()
        
        equals_pos = lines[1].find('t=')         # string manipulation to access raw temperature data
       
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0      # conversion to F (check ability to provide both)
        
        self.current_temp = temp_f
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        self.temp_logs[current_time] = self.current_temp
        
        
    def return_temp(self): 
     
        return self.current_temp
        
      
def arctic_spark(arr, time_out):
        for zone in arr:
                zone.get_temp()
                zone.temp_check()
                zone.gpio_output()
                
        time.sleep(time_out)
        
        
        
