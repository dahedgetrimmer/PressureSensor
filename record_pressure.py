from machine import Pin, I2C
from bmp085 import BMP180
import time
import utime

i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 35000)

utime.sleep_ms(1)

bmp = BMP180(i2c)
bmp.oversample=3
bmp.sealevel= 0

logf = open('ambient_press_log.csv', 'a')    #creates pressure log .csv
timestamp = 0                                #initialize timestamp
start_time= utime.ticks_ms()                 #start timer


#start recording in .csv file
while True:                                
    print(timestamp)                #prints the current timestamp in terminal
    pres_hPa = bmp.pressure         #assigns current station pressure (in hPa) to a variable
    
    try:
        logf.write(str(timestamp) + ',' + str(pres_hPa) + '\r\n')      #writes current timestamp and associated pressure reading into .csv file
    except OSerror:
        print('Disk FULL')            #if RaspberryPi storage capacity is exceeded.
     	break

    if timestamp >= 10:               #ends the pressure recording loop at set time limit (in seconds)
        break
    
    timestamp = utime.ticksdiff(utime.ticks_ms(), start_time)/1000            #calculate the next timestamp
    
    utime.sleep_ms(8)		#delay next reading by 8 ms to maintain microcontroller/sensor stability
    
logf.close()                    #closes .csv file
print(timestamp)                #verify final timestamp