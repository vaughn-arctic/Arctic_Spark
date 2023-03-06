#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 16:07:08 2022

@author: vaughn
"""

"""
- Create Device Name get code

- Create Data structure code

- Create functions code (Main) 

- GLOBAL VARIABLES
    - int temp low
    - string device name
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
    


"""
import time
import Rpi.GPIO as GPIO


class Temp_zone: 
    def __init__(self, sensor_ID, device,  GPIO_pin, low_temp_value):
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
        
        
        
        
        self.sensor_ID = sensor_ID # 28-bit sensor ID value for direct assignment
        self.device = device        # root directory of sensors
        self.GPIO_pin = GPIO_pin   # dedicated GPIO output pin -> to relay
        self.current_temp = 0       # initialized to 0, updates on get_temp()
        self.temp_logs = {
                            }       # stores get_temp() value : current_time
        
        self.threshold = low_temp_value + 5 # creates a 5 F degree buffer
        self.threshold_flag = False  # Flags if out of temperature bound and activates 
                                    #GPIO output pin 
                        
                                    
                        
                                    
    def temp_check(self):
        '''
        Comparees current temperature against minimu threshold
        
        Updates threshold flag to turn on our of
        
        
        '''
        if self.current_temp <= self.threshold:
            self.threshold_flag = True
        
        elif self.current_temp > self.threshold:
            self.threshold_flag = False
        
        
        
        
        
    def GPIO_output(self):
        '''
        Sends signal to dedicated GPIO_pin, to activate relay allowing heater assigned to 
        this thermal zone to turn on

        Returns
        -------
        None.

        '''
        
        
        
        GPIO.output(self.GPIO_pin, self.threshold_flag)
        
        
    def get_temp(self): 
        
        '''
        readlines() to get the temp
        
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
        
        
        
