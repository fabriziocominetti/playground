from random import seed
from random import randint
team1 = (input("Please enter home team: "))
team2 = (input("Please enter away team: "))
for i in range(5):
    score1 = randint(0,5)
for i in range(5):
    score2 = randint(0,5)
print("Final Score: "+team1.upper()+" "+str(score1)+" : "+team2.upper()+" "+str(score2))