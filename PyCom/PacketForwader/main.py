from network import LoRa
import socket
import ubinascii
import struct
import time
import pycom
import machine
from network import WLAN

# FOR : LoPy_1

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
setup_WiFi()
i=0
# create ABP authentication params
"""
dev_addr = struct.unpack(">l", ubinascii.unhexlify('01e34d9b'))[0]
nwk_swkey = ubinascii.unhexlify('aa731d1f1e080acd940efee9e4260368')
app_swkey = ubinascii.unhexlify('69e2c0b276f9e4529cc637e075227ffc')

"""
dev_addr = struct.unpack(">l", ubinascii.unhexlify('26011E59'))[0]
nwk_swkey = ubinascii.unhexlify('066D4FDDD8CE37307C2D90D23840912C')
app_swkey = ubinascii.unhexlify('3C2DD98C6D2B8D54B6052770857DDD63')

app_eui = ubinascii.unhexlify('70B3D57ED0013933') #  70B3D5499BB14247
app_key = ubinascii.unhexlify('86bb365ea411226b16dc36cc14bd06dd') #LoRaServer Network Key

while True:
    #data = bytes([0x01, 0x02, 0x03])

    set_LoRa_RAW()
    data = s.recv(64)
    while (data == b'') :
        data = s.recv(64)
        print(data)
        time.sleep(10)


    set_LoRa_WAN_OTAA()
    s.setblocking(True)
    blink()
    s.send(data)
    s.setblocking(False)
    print(i, "sent", data)
    time.sleep(10)
    i += 1
