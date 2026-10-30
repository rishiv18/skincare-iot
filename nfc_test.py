from machine import Pin, I2C
import time

i2c = I2C(
    0,
    sda=Pin(8),
    scl=Pin(9),
    freq=100_000
)

time.sleep(1)

devices = i2c.scan()
print("I2C devices:", [hex(address) for address in devices])

if 0x24 in devices:
    print("PN532 detected!")
else:
    print("PN532 not found. Check wiring and switches.")