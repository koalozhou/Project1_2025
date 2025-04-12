# Author: Yang Yue
# Date: 2025-04-12
# Quick Reaction Game

from gpiozero import LED, Button
from time import sleep, time
from random import uniform

# Hardware Configuration (Verify physical connections)
LED_PIN = 4
LEFT_BUTTON_PIN = 14  # Confirm with physical wiring
RIGHT_BUTTON_PIN = 15  # Confirm with physical wiring

# Initialize components
led = LED(LED_PIN)
left_button = Button(LEFT_BUTTON_PIN, pull_up=True, bounce_time=0.1)
right_button = Button(RIGHT_BUTTON_PIN, pull_up=True, bounce_time=0.1)

# Game settings
player_left = input("Left player name: ")
player_right = input("Right player name: ")
total_rounds = int(input("Number of rounds: "))

# Game state
scores = {player_left: 0, player_right: 0}
current_round = 0
game_active = False


def button_pressed(btn):
    global game_active
    if not game_active:
        return

    game_active = False  # Lock game state

    # Determine winner
    if btn.pin.number == LEFT_BUTTON_PIN:
        winner = player_left
    else:
        winner = player_right

    scores[winner] += 1
    print(f"\n[RESULT] {winner} wins this round!")
    print(f"[SCORE] {player_left}: {scores[player_left]} | {player_right}: {scores[player_right]}")


# Register button handlers
left_button.when_pressed = button_pressed
right_button.when_pressed = button_pressed

# Main game loop
while current_round < total_rounds:
    current_round += 1
    print(f"\n=== Round {current_round} ===")

    # Reset game state
    game_active = True
    led.off()

    # Random LED phase
    led.on()
    sleep(uniform(5, 10))
    led.off()

    # Response window
    start_time = time()
    timeout = 3

    while (time() - start_time < timeout) and game_active:
        sleep(0.05)

    # Handle timeout
    if game_active:
        print("[TIMEOUT] No response this round!")
        game_active = False

# Final results
print("\n=== Game Over ===")
print(f"[FINAL SCORE] {player_left}: {scores[player_left]} | {player_right}: {scores[player_right]}")
if scores[player_left] == scores[player_right]:
    print("[TIE] Game ends in draw!")
else:
    winner = max(scores, key=scores.get)
    print(f"[CHAMPION] {winner} wins!")

# Cleanup
led.close()
left_button.close()
right_button.close()