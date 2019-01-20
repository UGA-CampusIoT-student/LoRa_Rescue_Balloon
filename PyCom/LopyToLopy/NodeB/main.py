from network import LoRa
import socket
import time
import pycom

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915

pycom.heartbeat(False)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

while True:
    pycom.rgbled(0x7f0000)
    s.send('Ping')
    pycom.rgbled(0x00)
    time.sleep(5)