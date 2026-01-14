from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)

print("LED starts flashing...")
while True:
    led.on()
    sleep(2) # puts a delay of 2 seconds
    led.off()
    sleep(2)
pin.off()
print("Finished.")
