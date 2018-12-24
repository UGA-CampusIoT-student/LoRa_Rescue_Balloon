import pycom
import machine
import math
import network
import os
import time
import utime
import gc
import socket
import ubinascii
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pytrack import Pytrack
from network import LoRa

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)

time.sleep(2)
gc.enable()

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print('\nRTC Set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

py = Pytrack()
l76 = L76GNSS(py, timeout=30)

# sd = SD()
# os.mount(sd, '/sd')
# f = open('/sd/gps-record.txt', 'w')

def encodeCoordinate(number):

    """
    This function encodes the coordinates from float to 3 bytes form. 
    Better accuracy can be achieved by rewriting the function to use 4 instead of 3 bytes for encoding.
    The inverse procedure has to be performed to decode the coordinates on the application side.

    Documentation for best practises while encoding data for LoRa trasmition:

    https://www.thethingsnetwork.org/docs/devices/bytes.html
    https://www.thethingsnetwork.org/forum/t/best-practices-when-sending-gps-location-data/1242
    
    decimal   decimal    distance
    places    degrees   (in meters)
    -------  ---------  -----------
    1        0.1000000   11,057.43      11 km
    2        0.0100000    1,105.74       1 km
    3        0.0010000      110.57     100  m
    4        0.0001000       11.06      10  m
    5        0.0000100        1.11       1  m
    6        0.0000010        0.11      11 cm
    7        0.0000001        0.01       1 cm

    Latitude: -90 to 90 -> xxx.xxxx -> 3 bytes to encode
    Longitude: -180 to 180 -> xxxx.xxxx -> 3 bytes to encode
    
    """
    
    number = round(number, 4) # Rounding the coordinate to 4 decimal places, equivalent to a precision of 10m 
    number = int(number * 10000) # Multiplying the coordinate by 10000 in order to transform to an integer
    
    array = [None]*3 # Creating an array to store the bytes 
    
    hex_0 = 0xff0000
    hex_1 = 0x00ff00
    hex_2 = 0x0000ff
    
    array[0] = int ((number & hex_0) >> 4 * 4)
    array[1] = int ((number & hex_1) >> 4 * 2)
    array[2] = int (number& hex_2)
  
    return bytes(array) # returning the coordinate in byte format, necessary for LoRa transmition 

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, frequency=868100000) #forced frequency to 868.1 

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0013933')
app_key = ubinascii.unhexlify('5BBC57394313FC28C1056E73D974D87E')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)


# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')
pycom.rgbled(0xff8100)
print("CONNECTED")

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)
#lora.frequency(868100000)

coord = l76.coordinates()
latitude = coord[0]
longitude = coord[1]

s.send(bytes([0x01, 0x02, 0x03]))
s.send(bytes([0x01, 0x02, 0x03]))
s.send(bytes([0x01, 0x02, 0x03]))
print("Sent bytes")


while (longitude == None or latitude == None):
    print("No GPS signal")
    coord = l76.coordinates()
    latitude = coord[0]
    longitude = coord[1]

# send some data

s.send(encodeCoordinate(latitude))
s.send(encodeCoordinate(longitude))
print("Coordinates sent!")
pycom.rgbled(0x00FF00)

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)

while (True):
    coord = l76.coordinates()
    #f.write("{} - {}\n".format(coord, rtc.now()))
    print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))
