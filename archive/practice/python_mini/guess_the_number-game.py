# Guess the Number game

import random

number = random.randint(1,10)

for i in range(0,3):
    user = int(input("Guess the number"))
    if user == number:
        print("You did it!")
        print(f"You guessed the number right, it's {number}")
        break
    elif user > number:
        print("Your guess is too high")
    elif user < number:
        print("Your guess is too low")
else:
    print(f"Nice try :( , but the number is {number}")