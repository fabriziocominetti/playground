import math
import random

num_teams = 32
num_nations = 8 
#global variables
italy = []
england = []
germany = []
spain = []
france = []
portugal = []
netherlands = []
russia = []
turkey = []
belgium = []
ukraine = []
restofeurope = []

groupA = []
groupB = []
groupC = []
groupD = []
groupE = []
groupF = []
groupG = []
groupH =[]

groups = [groupA, groupB, groupC, groupD, groupE, groupF, groupG, groupH]
nations1 = [italy, england, germany, spain, france, portugal]
nations2 = [netherlands, russia, turkey, belgium, ukraine, restofeurope]
used = []
loading = 0
tens = 10

#intro
print("\tUEFA Champions League Draw Simulator\n")
print("Enter teams to make your very own draw")
input("Press the enter key to begin")

#ask for teams
italy += [input("Please enter an Italian team: ")]
italy += [input("Please enter an Italian team: ")]
italy += [input("Please enter an Italian team: ")]
italy += [input("Please enter an Italian team: ")]

england += [input("Please enter an English team: ")]
england += [input("Please enter an English team: ")]
england += [input("Please enter an English team: ")]
england += [input("Please enter an English team: ")]

germany += [input("Please enter a German team: ")]
germany += [input("Please enter a German team: ")]
germany += [input("Please enter a German team: ")]
germany += [input("Please enter a German team: ")]

spain += [input("Please enter a Spanish team: ")]
spain += [input("Please enter a Spanish team: ")]
spain += [input("Please enter a Spanish team: ")]
spain += [input("Please enter a Spanish team: ")]

france += [input("Please enter a French team: ")]
france += [input("Please enter a French team: ")]
france += [input("Please enter a French team: ")]

portugal += [input("Please enter a Portuguese team: ")]
portugal += [input("Please enter a Portuguese team: ")]
portugal += [input("Please enter a Portuguese team: ")]

netherlands += [input("Please enter a Dutch team: ")]
netherlands += [input("Please enter a Dutch team: ")]
netherlands += [input("Please enter a Dutch team: ")]

russia += [input("Please enter a Russian team: ")]

turkey += [input("Please enter a Turkish team: ")]

belgium += [input("Please enter a Belgian team: ")]

ukraine += [input("Please enter an Ukrainan team: ")]

restofeurope += [input("Please enter a Scottish/Greek/Danish/Austriac/Swiss/Crotian/RestofEurope team: ")]
restofeurope += [input("Please enter a Scottish/Greek/Danish/Austriac/Swiss/Crotian/RestofEurope team: ")]
restofeurope += [input("Please enter a Scottish/Greek/Danish/Austriac/Swiss/Crotian/RestofEurope team: ")]

#make copies
italy1 = italy[:]
england1 = england[:]
germany1 = germany[:]
spain1 = spain[:]
france1 = france[:]
portugal1 = portugal[:]
netherlands1 = netherlands[:]
russia1 = russia[:]
turkey1 = turkey[:]
belgium1 = belgium[:]
ukraine1 = ukraine[:]
restofeurope1 = restofeurope[:]

nations3 = [italy1, england1, germany1, spain1, france1, portugal1]
nations4 =[netherlands1, russia1, turkey1, belgium1, ukraine1, restofeurope1]

#create groups
while num_teams != 7:
    x = 0
    position = random.randrange(len(nations1))
    nation = nations1[position]
    nation1 = nations3[position]
    if nation1:
        team = random.choice(nation1)
        if team not in used:
            group = random.choice(groups)
            if len(group) < 4:
                for i in group:
                    if i not in nation:
                        x += 0
                    else:
                            x += 1
                    if x == 0:
                        group += [team]
                        num_teams -=1
                        used += [team]
                        nation.remove(team)
                        loading += 1
                        if loading == tens:
                            print("\nLoading...\n")
                            tens += 10
while num_teams != 0:
    x = 0
    position = random.randrange(len(nations2))
    nation = nations2[position]
    nation1 = nations4[position]
    if nation1:
        team = random.choice(nation1)
        if team not in used:
            group = random.choice(groups)
            if len(group) < 4:
                for i in group:
                    if i not in nation:
                        x += 0
                    else:
                        x += 1
                if x == 0:
                    group += [team]
                    num_teams -= 1
                    used += [team]
                    nation1.remove(team)
                    loading += 1
                    if loading == tens:
                        print("\nLoading...\n")
                        tens += 10

#display groups
print("\nAssembling groups...\n")
input("Groups complete, press the enter key to view")

print("\nGroup A")
print(groupA[0])
print(groupA[1])
print(groupA[2])
print(groupA[3])

print("\nGroup B")
print(groupB[0])
print(groupB[1])
print(groupB[2])
print(groupB[3])

print("\nGroup C")
print(groupC[0])
print(groupC[1])
print(groupC[2])
print(groupC[3])

print("\nGroup D")
print(groupD[0])
print(groupD[1])
print(groupD[2])
print(groupD[3])

print("\nGroup E")
print(groupE[0])
print(groupE[1])
print(groupE[2])
print(groupE[3])

print("\nGroup F")
print(groupF[0])
print(groupF[1])
print(groupF[2])
print(groupF[3])

print("\nGroup G")
print(groupG[0])
print(groupG[1])
print(groupG[2])
print(groupG[3])

print("\nGroup H")
print(groupH[0])
print(groupH[1])
print(groupH[2])
print(groupH[3])

# exit
input("\n\nPress the enter key to exit.")