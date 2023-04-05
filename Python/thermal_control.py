#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import glob
import os
import Rpi.GPIO as GPIO

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sensor_locations = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')
GPIO.setmode(GPIO.Board)
GPIO.setwarnings(False)
global gpio_pin_array = [ 22, 29, 31, 32, 35, 36, 37, 38]   # dedicated out-put pins available on raspberry pi 


class Temp_zone: 
    def __init__(self, sensor_ID, zone_ID gpio_signal_pin, low_temp_value):
        '''
        Parameters
        ----------
        sensor_ID : String: local_address+ID+/w1_slave
            sensor ID access address from the root directory
          
        zone_ID : Numeric value of zone
        
        GPIO_pin : int 
            dedicated GPIO output pin -> to relay
            
        low_temp_value : int
            Global variable input from user to establish lowest viable temperature

        Returns
        -------
        None.

        '''
        
        self.sensor_ID = sensor_ID
        self.zone_ID = zone_ID
        self.gpio_signal_pin = gpio_signal_pin                         
        self.current_temp = 0                                          
        self.temp_logs = { }                                            
        
        self.threshold = low_temp_value + ( 0.125 * low_temp_value)    
        # creates a 12.5% buffer above the minumum threshold 
        # This ensures heaters will activate before and wont shut off at once reaching minimums
        
        # !!!!! x =-y^{3} + 120
        # Rework this algebra so that lower low_temp_values have higher adjusted thresholds
                                        
        self.threshold_flag = False                                       
                                    
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
        Sends signal to dedicated GPIO_pin to control heating element
        '''
        GPIO.output(self.gpio_signal_pin, self.threshold_flag)
        
    def get_temp(self): 
        # Accessess raw temperature data in the form of a 2 line string from the DBS180 Sensor
        # Uses string manipulation & typecasting to retrieve the tempature reading
        try:
                
                with open(self.sensor_ID, 'r') as f:  
                        lines = f.readlines()
                        f.close()

                        temp_in_string = lines[1].find('t=')         
                        temp_string = lines[1][temp_in_string+2:]    
                        temp_c = float(temp_string) / 1000.0     
                        temp_f = (temp_c * 1.8) + 32                            #(check need to provide both C & F)

                        self.current_temp = temp_f

                        t = time.localtime()
                        current_time = time.strftime("%H:%M:%S", t)
                        self.temp_logs[current_time] = self.current_temp        
                        
        except FileNotFoundError:
            print(f"Sensor file for {self.sensor_id} not found.") 
        
        
    def return_temp(self): 
        return self.current_temp

    def return_status(self):
        return self.threshold_flag


def arctic_spark(arr):
        '''
        Main runtime function that itterates through sensor_array and performs required sensing, updated, output and data 
        recording functions for each temp_zone
        
        User defined timeout value (want to check w/ Ben about requirements
        '''
        for zone in arr:
                zone.get_temp()
                zone.temp_check()
                zone.gpio_output()
                print("Zone {} is currently {} degrees\n".format(zone.zone_ID, zone.return_temp)
                
                  
               #if zone.return_status == True:
               #       print("Zone is outside of threshold and is currently being heated\n\n")
               #else:
               #        print("Zone is within tolerance and is not being heated\n\n")
                ''
        time.sleep(3)
        
                       
                       '''
def set_sensor_config(): 
       
        Using user input values and global pin array, this function creates an array of Temp_Zone class instances
        with corresponding data
        
        i = 0
        for sensor in sensor_locations:
                sensor_array.append(Temp_zone(sensor, gpio_pin_array[i], temp_zone_lows[i]))
                i += 1
        '''

                       
if __name__ == "__main__": 
                       
                       
    sensor_array = []                   
    temp_zone_lows = [] 
    i = 0
    
    for x in range (0,8):
        user_input = int(input("Enter the minimum temperature(F) for zone {}:\t".format(x+1)))
        temp_zone_lows.append(user_input)
        
    for sensor in sensor_locations:
        sensor_array.append(Temp_zone(sensor, (i+1), gpio_pin_array[i], temp_zone_lows[i]))
        i += 1
 
    print("Initiating system operation\n") 
     
    try: 
        while(True):
            artcic_spark(sensor_array)
                      
    except KeyboardInterrupt:
        print("Operation Ended")
    
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
    
                      
                       
       
