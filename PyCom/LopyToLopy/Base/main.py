from network import LoRa
import socket
import time
import pycom
from network import WLAN

pycom.heartbeat(False)

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

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

while True:
    pycom.rgbled(0x00007f)
    print(s.recv(64)) 
    pycom.rgbled(0x00)
    time.sleep(5)