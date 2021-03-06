from network import LoRa
import socket
import time
import pycom
import machine
from network import WLAN

pycom.heartbeat(False)

"""
wlan = WLAN(mode=WLAN.STA)
ssid = "A8A"
wpaKey = "gerrikos24"

nets = wlan.scan()
for net in nets:
    if net.ssid == ssid:
        print('WiFi network found! ',)
        wlan.connect(net.ssid, auth=(net.sec, wpaKey), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded! ', wlan.ifconfig())
        break
"""

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

i=0

while True:
    pycom.rgbled(0x7f0000)
    data = s.recv(64)
    #print(data)
    if data == b'Ping':
        sendStr = data + " Pong " + str(i)
        s.send(sendStr)
        print("sent str")
    time.sleep(0.05)
    pycom.rgbled(0x00)
    time.sleep(5)
    i = i + 1