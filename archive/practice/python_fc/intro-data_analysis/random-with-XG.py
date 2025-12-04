import random

homeXG = [round(random.random(), 3), round(random.random(), 3), round(random.random(), 3)]
awayXG = [round(random.random(), 3), round(random.random(), 3), round(random.random(), 3)]

def calculateWinner(homeXG, awayXG):
    homeGoals = 0
    awayGoals = 0

    def testShots(shots):
        
        goals = 0
        
        # For each shot, if it goes in, add a goal
        for shot in shots:
            if random.random() <= shot:
                goals += 1
                
        return goals
        
    homeGoals = testShots(homeXG)
    awayGoals = testShots(awayXG)
    
    # Return the score
    if homeGoals > awayGoals:
        print("Home Wins! {} - {}".format(homeGoals, awayGoals))
    elif awayGoals > homeGoals:
        print("Away Wins! {} - {}".format(homeGoals, awayGoals))
    else:
        print("Share of the points! {} - {}".format(homeGoals, awayGoals))

calculateWinner(homeXG, awayXG)