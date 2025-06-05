import random

numbers = "0123456789"
lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # or lower.upper
special = "!#$%&()*+,-./:;?@[\]^_{|}~"

all = numbers + lower + upper + special

length = int(input("Select password length: "))

password = "".join(random.sample(all, length))
print(password)