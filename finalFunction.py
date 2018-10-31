import smbus
import math
import os
import time
import sys
import paho.mqtt.client as mqtt


THINGSBOARD_HOST = '172.21.216.242'



power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
def read_byte(adr):
    return bus.read_byte_data(address, adr)
 
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val
 
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command
bus.write_byte_data(address, power_mgmt_1, 0)


INTERVAL=2

sensor_data = {'accelerometer_x': 0, 'accelerometer_y': 0}

next_reading = time.time() 

client = mqtt.Client()
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()


try:
    while True:
	accel_xout = read_word_2c(0x3b)
	#accel_xout_scaled = accel_xout / 16384.0
	accel_yout = read_word_2c(0x3d)
	#accel_yout_scaled = accel_xout / 16384.0
        #humidity = round(humidity, 2)
        #temperature = round(temperature, 2)
        #print(u"accelerometer_x : {:g}\u00b0C, accelerometer_y : {:g}%".format(accelerometer_x , accelerometer_y ))
        #sensor_data['accelerometer_y '] = accelerometer_y 
        #sensor_data['accelerometer_x '] = accelerometer_x

        # Sending humidity and temperature data to Thingsboard
        client.publish('accelerometer_x', str(accel_xout ) )
	client.publish('accelerometer_y', str(accel_yout ) )
        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
