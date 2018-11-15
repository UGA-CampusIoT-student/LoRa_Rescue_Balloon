# Pycom LoPy LoRaWAN nano gateway

Adapted from https://docs.pycom.io/tutorials/lora/lorawan-nano-gateway
https://github.com/pycom/pycom-libraries.git
(examples/lorawan-nano-gateway/)

## Added
* LED blink while connecting to Wifi SSID network.
* LED blink while connecting to NTP server for setting time.
* LED blink while receiving a LoRa frame.


## Setup
* set SERVER and PORT into config.py
* set WIFI_SSID and WIFI_PASS into config.py
* set LORA_FREQUENCY, LORA_GW_DR and LORA_NODE_DR into config.py

## Installation
TBD

## Version

```bash
CURRENT_SHORT_COMMIT=$(git rev-parse --short HEAD)
echo $CURRENT_SHORT_COMMIT
c88fd9b
```

## TODOLIST
[ ] add GPS position of the gateway when the LoPy is on a PyTrack board (see https://github.com/brocaar/pycom-examples/tree/master/pytrack-example)

## Licence
Pycom Licence v2.2 
https://github.com/pycom/pycom-libraries/blob/master/license/Pycom%20Licences%20v2.2.pdf
