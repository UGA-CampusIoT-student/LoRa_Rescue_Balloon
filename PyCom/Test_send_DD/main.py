# CampusIoT :: Pycom program sample
# Author : Didier DONSEZ

from network import LoRa
from machine import RTC
import socket
import time
import pycom
import binascii

#from L76GNSS import L76GNSS
#from pytrack import Pytrack

import config

pycom.heartbeat(False)
rtc = RTC()

# Initialize PyTrack.
#py = Pytrack()
#l76 = L76GNSS(py, timeout=30)

# Initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, adr=True,
    public=True,
    tx_retries=2,
    device_class=LoRa.CLASS_A
    )

print('Boot at ', rtc.now())
print('Radio EUI=', binascii.hexlify(lora.mac()))
# create an OTAA authentication parameters

# Device ID: 240AC400C0CE
# LoRa MAC: 70B3D5499BDBEE28 (28EEDB9B49D5B370)

dev_eui = binascii.unhexlify('70B3D5499BB14247')
app_eui = binascii.unhexlify('817976f0d07cd25d999dc8dce626f0dd')
app_key = binascii.unhexlify('684e24b97b6d13853a6f9eeb12160d1f')

RED   = 0xff0000;
GREEN = 0x00ff00;
BLUE  = 0x0000ff;
ORANGE = 0xffa500;
CYAN = 0x00B7EB;
PINK = 0xFF69B4;
OFF   = 0x000000;

DATARATE = 0

while True:
    # join a network using OTAA (Over the Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key),
        #dr=config.LORA_NODE_DR,
        timeout=0, dr=DATARATE)
        # timeout: is the maximum time in milliseconds to wait for the Join Accept message to be received. If no timeout (or zero) is given, the call returns immediately and the status of the join request can be checked with lora.has_joined().
        # dr: is an optional value to specify the initial data rate for the Join Request. Possible values are 0 to 5 for EU868, or 0 to 4 for US915.
        # TODO start with dr=5, if timeout, try dr=4, ... until dr=0.
    pycom.rgbled(RED)
    Cont = True

    # wait until the module has joined the network
    while not lora.has_joined():
        time.sleep(1)
        pycom.rgbled(RED)
        time.sleep(0.1)
        pycom.rgbled(OFF)
        print('Not yet joined...')

    # TODO print('Joined with DevAddr=',)

    pycom.rgbled(GREEN)
    time.sleep(1)
    pycom.rgbled(OFF)

    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, DATARATE)

    # selecting confirmed type of messages
    s.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, True)

    # make the socket blocking
    s.setblocking(False)

    time.sleep(5.0)
    cpt = 0
    while Cont:
        #coord = l76.coordinates()
        #f.write("{} - {}\n".format(coord, rtc.now()))
        # print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))
        #print("{} - {}".format(coord, gc.mem_free()))

        pkt = bytes([cpt & 0xFF, (cpt >> 8) & 0xFF])
        # TODO add coordinates (if PyTrack), LIS2HH12 values for acc
        print('Sending:', pkt)
        s.send(pkt)
        pycom.rgbled(GREEN)
        time.sleep(0.1)
        pycom.rgbled(OFF)
        time.sleep(9)
        """
        
        rx, port = s.recvfrom(256)


        if rx:
            print('Received: {}, on port: {} ({})'.format(rx, port, lora.stats()))
            pycom.rgbled(BLUE)
            time.sleep(1)
            pycom.rgbled(OFF)
            # TODO special case for port=224 (set confirmation, ask for LinkCheck, force rejoin)
            # TODO port=123 (NTP) for setting RTC  rtc.init((2017, 2, 28, 10, 30, 0, 0, 0))
            # TODO port=?? for setting TX period, Acc threshhold, ...

            # if port=123, set RTC
            if port == 123:
                rtc.init((rx[0]+2000, rx[1], rx[2], rx[3], rx[4], rx[5], 0, 0))
                print('Set RTC at ', rtc.now())

            # if port=200, force to rejoin
            if port == 200:
                print('Rejoin in few seconds ...')
                pycom.rgbled(ORANGE)
                Cont = False

            # if port=201, selecting confirmed type of messages
            if port == 201:
                # selecting confirmed type of messages
                print('Select Confirmed')
                pycom.rgbled(CYAN)
                s.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, True)

            # if port=201, selecting confirmed type of messages
            if port == 202:
                # selecting unconfirmed type of messages
                print('Select Unconfirmed')
                pycom.rgbled(PINK)
                s.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, False)

                """

        cpt = cpt + 1
        if cpt > 65535:
            #  Rejoin after loop
            print('Rejoin in few seconds ...')
            pycom.rgbled(ORANGE)
            Cont = False
        time.sleep(10)
