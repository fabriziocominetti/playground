# Random Story Generator

import random

when = ['Yesterday', 'Last night', 'A few days ago', 'A few weeks ago', 'A few months ago', ' A long time ago']
who = ['a human', 'a dog', 'an animal', 'a monster', 'a cyclope']
name = ['Luke', 'Post', 'Colson', 'Mary', 'Zena']
residence = ['Milan', 'Italy', 'Europe', 'Madrid', 'Bruges', 'America', 'Australia']
went = ['cinema', 'university', 'school', 'football game']
happened = ['made a lot of friends', 'made a burger', 'found a secret key', 'found a misterious map', 'solved a mistery']

print(random.choice(when) + ', ' + random.choice(who) + ' that lived in ' + random.choice(residence) + ', went to the ' + random.choice(went) + ' and ' + random.choice(happened))