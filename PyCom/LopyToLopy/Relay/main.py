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

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915

from network import WLAN
wlan = WLAN(mode=WLAN.STA)

ssid = "SFR-87"
wpaKey = "j44418OQ"

nets = wlan.scan()
for net in nets:
    if net.ssid == ssid:
        print('WiFi network found! ',)
        wlan.connect(net.ssid, auth=(net.sec, wpaKey), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded! ', wlan.ifconfig())
        break

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

pycom.heartbeat(False)

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
    
    if number < 0 : # The if statement treats the case when the coordinate is negative 
        number = -number
        array[0] = (number>>16) & 0xff | 0b10000000 # we fill the first byte of the encoded message and the 24th bit is turned to 1 to signify a negative number 
    else :
        array[0] = (number>>16) & 0xff # filling byte 0

    array[1] = (number>>8) & 0xff # filling byte 1
    array[2] = number & 0xff # filling byte 2

    return bytes(array) # returning the coordinate in byte format, necessary for LoRa transmition 

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

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
print("Joined!")

"""
# create a LoRaWAN socket
sWan = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
print("create a LoRaWAN socket")

# set the LoRaWAN data rate
sWan.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
print("set the LoRaWAN data rate")


# create a LoRaRAW socket
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
#s.setblocking(False)
print("create a LoRaRAW socket")
"""
"""
while True:
    if s.recv(64) == b'Ping':
        pycom.rgbled(0x00007f)
        s.send('Pong')
    pycom.rgbled(0x00)
    time.sleep(5)
"""

while True:
    print("Entered while loop")
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
    print("Initialized LoraRaw")
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    print("Created socket")
    data = s.recv(64)
    print("Data received")

    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    print("Initialized LoraWan")
    #s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    print("create a LoRaWAN socket")
    
    pycom.rgbled(0x00007f)
    s.setblocking(True)
    s.send(bytes([0x01, 0x02, 0x03]))
    pycom.rgbled(0x00)
    time.sleep(5)
    s.setblocking(False)
    
    