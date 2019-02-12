from network import LoRa
import socket
import time
import pycom
from network import WLAN
import machine

#LoPy_2

pycom.heartbeat(False)
def blink():
    pycom.rgbled(0x7f0000)
    time.sleep(0.05)
    pycom.rgbled(0x00)

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

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, frequency=868100000, sf=7)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

while True:
    data = s.recv(64)
    if data == b'Ping':
         pycom.rgbled(0x007f00)

    print(data)
    time.sleep(5)
