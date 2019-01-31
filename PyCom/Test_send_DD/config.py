""" LoPy LoRaWAN configuration options """

import machine
import ubinascii
from network import LoRa

LORA_ADR = True
LORA_NODE_DR = 0
LORA_TX_RETRIES = 2
# LORA_DEVICE_CLASS = LoRa.CLASS_A

# TODO add LORA_NODE_DEVEUI, LORA_NODE_APPEUI, LORA_NODE_APPKEY
