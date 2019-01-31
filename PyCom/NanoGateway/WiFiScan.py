from network import WLAN
wlan = WLAN(mode=WLAN.STA)

ssid = "Eddy-Malou"
wpaKey = "DRFM163CWXFE"

nets = wlan.scan()
for net in nets:
    if net.ssid == ssid:
        print('Network found! ',)
        wlan.connect(net.ssid, auth=(net.sec, wpaKey), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded! ', wlan.ifconfig())
        break