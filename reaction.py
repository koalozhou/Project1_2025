# Author: Renjie Zhou
# Date: 2025-04-09
# Random control the LED

from gpiozero import LED, Button
from time import sleep
from random import uniform

led = LED(4)

led.on()
sleep(uniform(5,10))
led.off()
