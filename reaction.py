# Author: Yang Yue
# Date: 2025-04-12
# Quick Reaction Game with Reaction Timer

from gpiozero import LED, Button
from time import sleep, time
from random import uniform

# Hardware Configuration (Verify physical connections)
LED_PIN = 4
LEFT_BUTTON_PIN = 14  # GPIO14 for left button
RIGHT_BUTTON_PIN = 15  # GPIO15 for right button

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
reaction_times = []
current_round = 0
game_active = False
start_time = 0


def button_pressed(btn):
    global game_active, start_time
    if not game_active:
        return

    game_active = False  # Lock game state

    # Calculate reaction time
    end_time = time()
    reaction_time = end_time - start_time
    reaction_time = round(reaction_time, 3)  # Precision to milliseconds

    # Store reaction time
    reaction_times.append(reaction_time)

    # Determine winner
    winner = player_left if btn.pin.number == LEFT_BUTTON_PIN else player_right
    scores[winner] += 1

    # Print results
    print(f"\n[RESULT] {winner} wins in {reaction_time} seconds!")
    print(f"[SCORE] {player_left}: {scores[player_left]} | {player_right}: {scores[player_right]}")


# Register button handlers
left_button.when_pressed = button_pressed
right_button.when_pressed = button_pressed

# Main game loop
try:
    while current_round < total_rounds:
        current_round += 1
        print(f"\n=== Round {current_round} ===")

        # Reset game state
        game_active = True
        led.off()  # Ensure LED starts off

        # Random LED phase
        led.on()
        delay = uniform(5, 10)
        sleep(delay)
        led.off()

        # Start reaction timer
        start_time = time()

        # Response window (3 seconds)
        timeout = 3
        while (time() - start_time < timeout) and game_active:
            sleep(0.05)

        # Handle timeout
        if game_active:
            print("[TIMEOUT] No response this round!")
            game_active = False

finally:
    # Ensure LED turns off on exit
    led.off()

# Final results
print("\n=== Game Over ===")
print(f"[FINAL SCORE] {player_left}: {scores[player_left]} | {player_right}: {scores[player_right]}")
if reaction_times:
    avg_time = round(sum(reaction_times) / len(reaction_times), 3)
    print(f"[STATS] Average reaction time: {avg_time} seconds")
else:
    print("[STATS] No valid reaction times recorded")

if scores[player_left] == scores[player_right]:
    print("[TIE] Game ends in draw!")
else:
    winner = max(scores, key=scores.get)
    print(f"[CHAMPION] {winner} wins!")

# Cleanup
led.close()
left_button.close()
right_button.close()