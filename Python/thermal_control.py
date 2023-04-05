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

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sensor_locations = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')
sensor_array = []
temp_zone_lows = []
GPIO.setmode(GPIO.Board)
GPIO.setwarnings(False)
global gpio_pin_array = [ 22, 29, 31, 32, 35, 36, 37, 38]   # dedicated out-put pins available on raspberry pi 

'''
                                Still working on the spatial requirments of this. 
                                Currently an 8 zone model (2 x 2 x 2 zones [18" x 18" x 18"] ) 
                                Consideration given to allowing user multi-modes (8 zone v. 16 zone) 
                                Include all GPIO pins and account for Temp_zone creation based upon 
                                combining multiple zones / sensors into a single class instance
                                Methods from the class are echoed to all hardware attached


'''

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
        
        self.sensor_ID = sensor_ID                                      # String
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
        ### Accessess raw temperature data in the form of a 2 line string from the DBS
        try:
                
                with open(self.sensor_ID, 'r') as f:  # read in current data from dedicated sensor
                        lines = f.readlines()
                        f.close()

                        temp_in_string = lines[1].find('t=')         # string manipulation to access raw temperature data from sensor
                        temp_string = lines[1][temp_in_string+2:]    # which is the last 4 values of the first string returned from the 
                        temp_c = float(temp_string) / 1000.0     # sensor, typecasted to a floating integer
                        temp_f = (temp_c * 1.8) + 32             # conversion to F (check requirement to provide both)

                        self.current_temp = temp_f

                        t = time.localtime()
                        current_time = time.strftime("%H:%M:%S", t)
                        self.temp_logs[current_time] = self.current_temp        # update temperature log with current reading
                        
        except FileNotFoundError:
            print(f"Sensor file for {self.sensor_id} not found.") 
        
        
    def return_temp(self): 
        return self.current_temp

    def return_status(self):
        return self.threshold_flag
        
      


def arctic_spark(arr, time_out: int):
        '''
        Main runtime function that itterates through sensor_array and performs required sensing, updated, output and data 
        recording functions for each temp_zone
        
        User defined timeout value (want to check 
        '''
        for zone in arr:
                zone.get_temp()
                zone.temp_check()
                zone.gpio_output()
                printf("Zone is currently {} degrees\n".format(zone.return_temp)
                
                '''       
               if zone.return_status == True:
                       printf("Zone is outside of threshold and is currently being heated\n\n")
               else:
                       printf("Zone is within tolerance and is not being heated\n\n")
                '''
        time.sleep(time_out)
        
def get_sensor_config(): 
        '''
        Using user input values and global pin array, this function creates an array of Temp_Zone class instances
        with corresponding data'''
        i = 0
        for sensor in sensor_locations:
                sensor_array.append(Temp_zone(sensor, gpio_pin_array[i], temp_zone_lows[i]
                i += 1
        
       
if __name__ == '__main__': 
        
      ### Prompt user for 8 zones
      # create zone_array
      # while loop arctic spark 
        # exit on keyboard input
                                              
      ''' 
      This main program is simply for testing.
      There is more complexity to be coded here as we develop our UI and are able to integrate it to this control system
      '''
