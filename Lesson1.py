import random

print("🏰 Welcome to Dungeon Number Guess!")
print("Guess the secret number to survive the dungeon.\n")

score = 0
round_number = 1
playing = True

while playing:
    print(f"\n--- Round {round_number} ---")
    
    max_number = round_number * 5
    secret_number = random.randint(1, max_number)
    
    attempts = 3
    
    for attempt in range(1, attempts + 1):
        guess = int(input(f"Attempt {attempt}/{attempts} - Guess a number (1 to {max_number}): "))

        if guess == secret_number:
            print("✅ Correct! You survived the dungeon.")
            score += 10
            break
        elif guess < secret_number:
            print("⬆️ Too low!")
        else:
            print("⬇️ Too high!")
    else:
        print(f"💀 You failed! The number was {secret_number}.")
        score -= 10

    print(f"Current Score: {score}")

    choice = input("Do you want to play another round? (y/n): ").lower()
    
    if choice != 'y':
        playing = False
    else:
        round_number += 1

print("\n🏁 Game Over")
print(f"Final Score: {score}")
#example game