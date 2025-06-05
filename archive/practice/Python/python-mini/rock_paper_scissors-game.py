# Rock, Paper & Scissors game

import random

options = ["Rock", "Paper", "Scissors"]
computer = random.choice(options)
player = False

cpu_score = 0
player_score = 0

while True:
    player = input("Select: Rock, Paper or Scissors?").capitalize()
    # Conditions of the game
    if player == computer:
        print("Tie!")
    elif player == "Rock":
        if computer == "Paper":
            print("You lose!", computer, "covers", player)
            cpu_score += 1
        else:
            print("You win!", player, "smashes", computer)
            player_score += 1
    elif player == "Paper":
        if computer == "Scissors":
            print("You lose!", computer, "cut", player)
            cpu_score+=1
        else:
            print("You win!", player, "covers", computer)
            player_score+=1
    elif player == "Scissors":
        if computer == "Rock":
            print("You lose!", computer, "smashes", player)
            cpu_score+=1
        else:
            print("You win!", player, "cut", computer)
            player_score+=1
    elif player == 'E':
        print("Final Scores:")
        print(f"CPU:{cpu_score}")
        print(f"PLAYER:{player_score}")
        break
    else:
        print("Not a valid play. Check your spelling!")
    computer = random.choice(options)