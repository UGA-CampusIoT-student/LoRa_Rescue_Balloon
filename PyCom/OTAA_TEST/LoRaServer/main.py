from network import LoRa
import socket
import time
import ubinascii
import time
import pycom

pycom.heartbeat(False)

# Initialise LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0013933')
app_key = ubinascii.unhexlify('86bb365ea411226b16dc36cc14bd06dd')
dev_eui = ubinascii.unhexlify('70B3D5499874B600')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

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
    s.send(bytes([0x01]))
    print("sent: ", bytes([0x01]))

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    time.sleep(10)