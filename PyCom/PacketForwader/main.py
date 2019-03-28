from network import LoRa
import socket
import ubinascii
import struct
import time
import pycom
import machine
from network import WLAN


# FUNTIONS
def setup_WiFi():
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
def blink():
    pycom.rgbled(0x7f0000)
    time.sleep(0.05)
    pycom.rgbled(0x00)
def set_LoRa_RAW():
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, frequency=868100000, sf=7)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
def set_LoRa_WAN_ABP():
    print("Setting up ABP...")
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
def set_LoRa_WAN_OTAA():
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    while not lora.has_joined():
        time.sleep(2)
        print('Not yet joined...')
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)


# INITIALIZATION
pycom.heartbeat(False)
#setup_WiFi()
i=0

# create ABP authentication params
dev_addr = struct.unpack(">l", ubinascii.unhexlify('01b1ece1'))[0]
nwk_swkey = ubinascii.unhexlify('3fcdf1f83a33d46dea2019f5bd01c79a')
app_swkey = ubinascii.unhexlify('869e6ec1ef8871d897890b8227f3d6a5')

"""
dev_addr = struct.unpack(">l", ubinascii.unhexlify('26011CAE'))[0]
nwk_swkey = ubinascii.unhexlify('F27AC96F79930C27726B7E7EFF5C3A50')
app_swkey = ubinascii.unhexlify('4A3D58478336A90A32B918E65C541772')
"""
app_eui = ubinascii.unhexlify('70B3D57ED0013933') #  70B3D5499BB14247
app_key = ubinascii.unhexlify('8e86f5cf7f56742f708cdedd79d6ec3d') #LoRaServer Network Key


while True:
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, frequency=868100000, sf=7)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)

    data = s.recv(64) #Listening 
    while (data == b''): #Waiting for data
        data = s.recv(64)
        print(data)
        time.sleep(10)

    print("Setting up ABP...")
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    
    s.setblocking(True)
    blink()
    s.send(data)
    s.setblocking(False)
    print(i, "sent", data)
    
    time.sleep(10)
    i += 1
    
