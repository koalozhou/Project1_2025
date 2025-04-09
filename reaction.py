# Author: Renjie Zhou
# Date: 2025-04-09
# Controlling the light

from gpiozero import LED, Button
from time import sleep

led = LED(4)

led.on()
sleep(5)
led.off()
