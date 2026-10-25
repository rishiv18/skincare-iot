
import network
import time
import sys

print("MicroPython:", sys.version)

wifi = network.WLAN(network.STA_IF)

try:
    print("Disabling Wi-Fi...")
    wifi.active(False)
    time.sleep(3)

    print("Enabling Wi-Fi...")
    wifi.active(True)
    time.sleep(3)

    print("Wi-Fi active:", wifi.active())

    print("Scanning networks...")
    networks = wifi.scan()

    for net in networks:
        print(
            "SSID:", net[0].decode("utf-8", "replace"),
            "| Signal:", net[3], "dBm"
        )

except Exception as e:
    print("ERROR:", repr(e))
