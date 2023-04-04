import glob
import time

# Define the location of the DS18B20 sensors
sensor_locations = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')


def read_temperature(location):
    # Open the file that contains the temperature reading
    with open(location, 'r') as f:
        lines = f.readlines()

    # Parse the temperature from the file
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temperature(location)

    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temperature_string = lines[1][equals_pos+2:]
        temperature_celsius = float(temperature_string) / 1000.0
        return temperature_celsius


# Read the temperature from each sensor and print the results
for location in sensor_locations:
    temperature = read_temperature(location)
    print('Temperature: {}C'.format(temperature))
