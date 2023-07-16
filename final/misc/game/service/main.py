#!/usr/local/bin/python

import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from scipy.optimize import linprog
from random import choice, uniform

from secrets import randbelow

def choose_rand(arr):
    t = uniform(0, 1)
    for tt in range(len(arr)):
        if (t <= arr[tt]):
            return tt
        t -= arr[tt]
    return len(arr) - 1

print("Initializing...")

FLAG = b'grey{Hey_you_are_good_at_this_game!__Yq9myj3kYTurr6Cr}'

server = []

M = [[randbelow(50) * (-1)**randbelow(2) for j in range(128)] for i in range(128)]
MT = [[-M[j][i] for j in range(128)] for i in range(128)]

A = []

for i in range(128):
    row = []
    for j in range(128):
        row.append(-MT[j][i])
    row.append(1)
    A.append(row)

A.append([1 for _ in range(128)] + [0])
A.append([-1 for _ in range(128)] + [0])

bounds = [(0, None) for _ in range(128)] + [(None, None)]

c = [0 for _ in range(128)] + [-1]
b = [0 for _ in range(128)] + [1, -1]

result = linprog(c, A_ub=A, b_ub=b, bounds=bounds)   
serverAdv = -result["fun"]

server = result['x']

print(f"payoff = {M}")

print('''
       .-------.    ______
      /   o   /|   /\     \\
     /_______/o|  /o \  o  \\
     | o     | | /   o\_____\\
     |   o   |o/ \o   /o    /
     |     o |/   \ o/  o  /
jgs  '-------'     \/____o/      
''')

print("Let's play a simple gambling game. You start with $200 in your account\n")
print("For each round, (10000 rounds maximum)")
print("1. Both of us choose a number between 0 to 127.")
print("2. Let the number you choose to be a, the number I choose to be b") 
print("3. Your savings will change by payoff[a][b]\n")
print("If you have no money left in your account, you lose.")
print("If you got at least $10000 at the end of a round, I will give you the flag\n")
print("Note: I will not cheat. I will not choose my number based on your curent input.\n")

money = 200
server2 = [i for i in range(128)]

inputs = [] 

for round in range(1, 10001):
    print(f"Round {round}:")
    print("What's your number?")
    s = int(input())
    if (len(inputs) >= 3):
        if (randbelow(2)):
            tt = choice(inputs[-3:])
            mini = 100
            k = 0
            for i in range(128):
                if (M[tt][i] < mini):
                    mini = M[tt][i]
                    k = i
        else:
            k = choose_rand(server)
    else:
        k = choose_rand(server)
    inputs.append(s)
    money += M[s][k]
    print(f"My selection was {k}, the change in your saving is payoff[{s}][{k}] = {M[s][k]}")
    print(f"You have ${money} in your account")
    
    if (money >= 10000):
        print(f"Congratulations! Here's your flag {FLAG}")
        exit(0)
    if (money <= 0):
        print("You are broke! Try again next time")
        exit(0)

print("Too many rounds for today. Try again next time")