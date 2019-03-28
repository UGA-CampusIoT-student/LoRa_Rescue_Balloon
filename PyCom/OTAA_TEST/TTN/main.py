from network import LoRa
import socket
import time
import ubinascii
import time
import pycom

pycom.heartbeat(False)

# Initialise LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, sf=7)

for i in range(0, 10):
    lora.remove_channel(i)

for i in range(0, 3):
    lora.add_channel(index=i, frequency=868100000, dr_min=0, dr_max=5)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0013933')
app_key = ubinascii.unhexlify('AB0560FE7E5F256096F7A85C41BA9BD3')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network

while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')
print('Joined')

while True:
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)

    # send some data
    s.send(bytes([0x01, 0x02, 0x03]))
    print("sent")

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    time.sleep(10)