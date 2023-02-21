#
# So most of this was written by a non-CS person, but it shows the basic method for not only communicating with one DBS1280 sensor, but multiple 
# I think he used 9 here, which is around the number we'd like to use
#
# The code for outputing temps is also here which will help set up either the LCD Display or IOT backend we set up 
#
# If we refactor and optimize this we could get it down to probably like 3-4 functions 
#
# the amazing guy even put a schematic of how to wire up multiple sensors to a single rasberry pi 
#
# And if we could see here if we can also implement the data class as well as the heating functions I think this might be all we need

# https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0


import os
import glob
import time

# These  lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
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


device_file = device_folder + '/w1_slave'
device_file1 = device_folder1 + '/w1_slave'
device_file2 = device_folder2 + '/w1_slave'
device_file3 = device_folder3 + '/w1_slave'
device_file4 = device_folder4 + '/w1_slave'
device_file5 = device_folder5 + '/w1_slave'
device_file6 = device_folder6 + '/w1_slave'
device_file7 = device_folder7 + '/w1_slave'
device_file8 = device_folder8 + '/w1_slave'


def read_rom():
    name_file = device_folder+'/name'
    f = open(name_file,'r')
    #print('f:',f)
    return f.readline()


def read_rom1():
    name_file1 = device_folder1+'/name'
    g = open(name_file1,'r')
    #print('g:',g)
    return g.readline()

def read_rom2():
    name_file2 = device_folder2+'/name'
    h = open(name_file2,'r')
    #print('h:',h)
    return h.readline()

def read_rom3():
    name_file3 = device_folder3+'/name'
    i = open(name_file3,'r')
    #print('i:',i)
    return i.readline()

def read_rom4():
    name_file4 = device_folder4+'/name'
    j = open(name_file4,'r')
    #print('j:',j)
    return j.readline()

def read_rom5():
    name_file5 = device_folder5+'/name'
    k = open(name_file5,'r')
    #print('k:',k)
    return k.readline()

def read_rom6():
    name_file6 = device_folder6+'/name'
    l = open(name_file6,'r')
    #print('l:',l)
    return l.readline()

def read_rom7():
    name_file7 = device_folder7+'/name'
    m = open(name_file7,'r')
    #print('m:',m)
    return m.readline()

def read_rom8():
    name_file8 = device_folder8+'/name'
    n = open(name_file8,'r')
    #print('n:',n)
    return n.readline()

#reading temperature from folder

 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    #print('raw_f',lines)
    f.close()
    return lines

def read_temp_raw1():
    g = open(device_file1, 'r')
    lines1 = g.readlines()
    #print('raw_g',lines1)
    g.close()
    return lines1

def read_temp_raw2():
    h = open(device_file2, 'r')
    lines2 = h.readlines()
    #print('raw_h',lines2)
    h.close()
    return lines2

def read_temp_raw3():
    i = open(device_file3, 'r')
    lines3 = i.readlines()
    #print('raw_i',lines3)
    i.close()
    return lines3

def read_temp_raw4():
    j = open(device_file4, 'r')
    lines4 = j.readlines()
    #print('raw_j',lines4)
    j.close()
    return lines4

def read_temp_raw5():
    k = open(device_file5, 'r')
    lines5 = k.readlines()
    #print('raw_k',lines5)
    k.close()
    return lines5


def read_temp_raw6():
    l = open(device_file6, 'r')
    lines6 = l.readlines()
    #print('raw_l',lines6)
    l.close()
    return lines6


def read_temp_raw7():
    m = open(device_file7, 'r')
    lines7 = m.readlines()
    #print('raw_m',lines7)
    m.close()
    return lines7

def read_temp_raw8():
    n = open(device_file8, 'r')
    lines8 = n.readlines()
    #print('raw_n',lines8)
    n.close()
    return lines8

#converting the temperature data to human readable form

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def read_temp1():
    lines1 = read_temp_raw1()
    while lines1[1].strip()[-3:] != 'YES':
        lines1 = read_temp_raw1()
        equals_pos1 = lines1[1].find('t=')
        temp_string1 = lines1[1][equals_pos1 +2:]
        temp_c1 = float(temp_string1) / 1000.0
        temp_f1 = temp_c1 * 9.0 / 5.0 + 32.0
        return temp_c1, temp_f1

def read_temp2():
    lines2 = read_temp_raw2()
    while lines2[2].strip()[-3:] != 'YES':
        lines2 = read_temp_raw2()
        equals_pos2 = lines2[1].find('t=')
        temp_string2 = lines2[1][equals_pos2 +2:]
        temp_c2 = float(temp_string2) / 1000.0
        temp_f2 = temp_c2 * 9.0 / 5.0 + 32.0
        return temp_c2, temp_f2

def read_temp3():
    lines3 = read_temp_raw3()
    while lines3[3].strip()[-3:] != 'YES':
        lines3 = read_temp_raw3()
        equals_pos3 = lines3[1].find('t=')
        temp_string3 = lines3[1][equals_pos3 +2:]
        temp_c3 = float(temp_string3) / 1000.0
        temp_f3 = temp_c3 * 9.0 / 5.0 + 32.0
        return temp_c3, temp_f3

def read_temp4():
    lines4 = read_temp_raw4()
    while lines4[4].strip()[-3:] != 'YES':
        lines4 = read_temp_raw4()
        equals_pos4 = lines4[1].find('t=')
        temp_string4 = lines4[1][equals_pos4 +2:]
        temp_c4 = float(temp_string4) / 1000.0
        temp_f4 = temp_c4 * 9.0 / 5.0 + 32.0
        return temp_c4, temp_f4

def read_temp5():
    lines5 = read_temp_raw5()
    while lines5[5].strip()[-3:] != 'YES':
        lines5 = read_temp_raw5()
        equals_pos5 = lines5[1].find('t=')
        temp_string5 = lines5[1][equals_pos5 +2:]
        temp_c5 = float(temp_string5) / 1000.0
        temp_f5 = temp_c5 * 9.0 / 5.0 + 32.0
        return temp_c5, temp_f5
    
def read_temp6():
    lines6 = read_temp_raw6()
    while lines6[6].strip()[-3:] != 'YES':
        lines6 = read_temp_raw6()
        equals_pos6 = lines6[1].find('t=')
        temp_string6 = lines6[1][equals_pos6 +2:]
        temp_c6 = float(temp_string6) / 1000.0
        temp_f6 = temp_c6 * 9.0 / 5.0 + 32.0
        return temp_c6, temp_f6

def read_temp7():
    lines7 = read_temp_raw7()
    while lines7[7].strip()[-3:] != 'YES':
        lines7 = read_temp_raw7()
        equals_pos7 = lines7[1].find('t=')
        temp_string7 = lines7[1][equals_pos7 +2:]
        temp_c7 = float(temp_string7) / 1000.0
        temp_f7 = temp_c7 * 9.0 / 5.0 + 32.0
        return temp_c7, temp_f7

def read_temp8():
    lines8 = read_temp_raw8()
    while lines8[8].strip()[-3:] != 'YES':
        lines8 = read_temp_raw8()
        equals_pos8 = lines8[1].find('t=')
        temp_string8 = lines8[1][equals_pos8 +2:]
        temp_c8 = float(temp_string8) / 1000.0
        temp_f8 = temp_c8 * 9.0 / 5.0 + 32.0
        return temp_c8, temp_f8

while True:
    #READING TEMPERATURE DATA AND PRINTINTING THE VALUES OF INDIVIDUAL 
SENSOR
    print(' C1=%3.3f  F1=%3.3f'% read_temp())
    print(' C2=%3.3f  F2=%3.3f'% read_temp1())
    print(' C3=%3.3f  F3=%3.3f'% read_temp2())
    print(' C4=%3.3f  F4=%3.3f'% read_temp3())
    print(' C5=%3.3f  F5=%3.3f'% read_temp4())
    print(' C6=%3.3f  F6=%3.3f'% read_temp5())
    print(' C7=%3.3f  F7=%3.3f'% read_temp6())
    print(' C8=%3.3f  F8=%3.3f'% read_temp7())
    print(' C9=%3.3f  F9=%3.3f'% read_temp8())
    time.sleep(1)
