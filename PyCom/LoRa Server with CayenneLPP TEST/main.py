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

from CayenneLPP import CayenneLPP

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)

time.sleep(2)
gc.enable()


# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0013933')
app_key = ubinascii.unhexlify('684e24b97b6d13853a6f9eeb12160d1f') #LoRaServer Network Key

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    #lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    time.sleep(2)
    print('Not yet joined...')
pycom.rgbled(0xff8100)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

while True:
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    
    lpp = CayenneLPP()
    
    lpp.add_temperature(1, 23.54)
    s.send(bytes(lpp.get_buffer()))
    s.setblocking(False)
    print("TEMP SENT!")

    time.sleep(30)


