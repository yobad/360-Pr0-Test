"""
Name: Teacher JAC
Description: Ultrasound, servo and motion detection garbage lid simulation
Date: 15-JAN-2026
"""

from machine import Pin, PWM
import time
from hcsr04 import HCSR04

# Parameters to finetune with hardware testing
THRESHOLD: float = 100 #minimum distance for determining if object is close
OPENED: int = 90
CLOSED: int = 0

max_duty = 7864
min_duty = 1802

# Initializing the PIR sensor
pir_pin = Pin(0, Pin.OUT)
# Initializing the ultrasound sensor with the appropriate trigger and echo pins
ultrasound_sensor = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=30000)

servo_pin = Pin(28, Pin.OUT)
servo_pwd = PWM(servo_pin, freq=50, duty_u16=max_duty)

# Function to convert angle to PWM duty
def angle_to_duty(angle):
    """Converts an angle of rotation of the SG90 into a duty cycle value
    source: https://apmonitor.com/dde/index.php/Main/ServoControl
    """
    return int(min_duty + (angle / 180.0) * (max_duty - min_duty))

def main():
    duty = angle_to_duty(CLOSED)
    servo_pwd.duty_u16(duty)
    while True:
        try:
            print("Reading distance...")
            distance_mm = ultrasound_sensor.distance_cm()
            is_moving = pir_pin.value()
            if (distance_mm <= THRESHOLD) and is_moving:
                print("Opened")
                duty = angle_to_duty(OPENED)
                servo_pwd.duty_u16(duty)
                print("Done throwing trash...")
            else:
                print("Closed")
                duty = angle_to_duty(CLOSED)
                servo_pwd.duty_u16(duty)
            print("Distance: ", distance_mm, "mm")
            print("Motion: ", is_moving)
        except Exception as e:
            print(e)
            break
        
        # wait time before next reading
        time.sleep(1)

if __name__ == "__main__":
    main()