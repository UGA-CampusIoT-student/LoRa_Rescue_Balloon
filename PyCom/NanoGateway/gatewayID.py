from network import WLAN
import ubinascii
wl = WLAN()
print(ubinascii.hexlify(wl.mac())[:6] + 'FFFE' + ubinascii.hexlify(wl.mac())[6:])