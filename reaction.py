# Author: Renjie Zhou
# Date: 2025-04-12
# Loop game

from gpiozero import LED, Button
from time import sleep
from random import uniform

led = LED(4)
# 确保左按钮接GPIO14，右按钮接GPIO15（关键修正点）
left_button = Button(14)  
right_button = Button(15)  

left_name = input('Left player name: ')
right_name = input('Right player name: ')

def pressed(button):
    # 调试：打印触发的引脚编号
    print(f"Button pressed on pin: {button.pin.number}")  
    if button.pin.number == 14:  # 左按钮触发
        print(f"{left_name} won the game!")
    else:  # 右按钮触发（引脚15）
        print(f"{right_name} won the game!")
    # 移除事件监听，避免重复触发
    left_button.when_pressed = None  
    right_button.when_pressed = None  

max_rounds = int(input("How many rounds do you want to play? "))
current_round = 0

while current_round < max_rounds:
    current_round += 1
    print(f"\nRound {current_round} begins!")
    
    # 重置事件监听
    left_button.when_pressed = pressed  
    right_button.when_pressed = pressed  
    
    led.on()
    delay = uniform(5, 10)  # 随机亮灯时间（5-10秒）
    sleep(delay)
    led.off()
