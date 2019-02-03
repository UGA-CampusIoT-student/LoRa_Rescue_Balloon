from network import LoRa
import socket
import ubinascii
import struct
import time
import pycom
import machine

pycom.heartbeat(False)

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915

# create an ABP authentication params
dev_addr = struct.unpack(">l", ubinascii.unhexlify('01722b4e'))[0]
nwk_swkey = ubinascii.unhexlify('7becb1a5d590aa874d4c748c100067e5')
app_swkey = ubinascii.unhexlify('56142806713f62f9bc79d741f8e50a7b')

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)


while(True):
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)

    pycom.rgbled(0x7f0000)
    time.sleep(0.05)
    pycom.rgbled(0x00)

    # send some data
    s.send(bytes([0x01, 0x02, 0x03]))

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print(data)

    time.sleep(1)

