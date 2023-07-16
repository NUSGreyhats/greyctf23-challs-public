#!/usr/local/bin/python
import random
from datetime import datetime
random.seed(datetime.now().timestamp())

turn = 0
isGameEnd = False

FLAG = "grey{tH3_n1mbLE_n4M_n0mNom_MY_nUmneMn0M}"

MIN_PILES = 30
MAX_PILES = 50
MIN_SIZE = 1
MAX_SIZE = 50_000
PRECISION = 1000

PILES = random.randint(MIN_PILES, MAX_PILES)
state = [random.randint(MIN_SIZE, MAX_SIZE) / PRECISION for _ in range(PILES)]

print(f"These are the piles and their numbers:")
print(state)
print()

L, R = 0.0, random.randint(2, MAX_SIZE // 2) / PRECISION

print(f"The bot has decided an upper bound of {R}")
L = float(input("Pick your lower bound: "))
while L > R or L <= 0:
	print("Haiya, lower bound cannot be greater than upper bound...")
	L = float(input("Pick your lower bound: "))
print()

scaled_L = round(L * PRECISION)
scaled_R = round(R * PRECISION)
scaled_LR = round((L + R) * PRECISION)
def getBotInput():
	grundy = 0
	for i in range(len(state)):
		scaled_state = round(state[i] * PRECISION)
		grundy ^= (scaled_state % scaled_LR) // scaled_L

	if grundy == 0:
		pile = random.randint(0, len(state)-1)
		while state[pile] < L:
			pile = random.randint(0, len(state)-1)
		num = random.randint(scaled_L, round(min(state[pile], R) * PRECISION))
		return str(pile), str(round(num / PRECISION, 3))
	
	for pile in range(len(state)):
		for num in range(scaled_L, min(scaled_R, round(state[pile] * PRECISION)) + 1):
			# calculate grundy value
			grundy = 0
			for i in range(len(state)):
				scaled_state = round(state[i] * PRECISION)
				if i == pile: grundy ^= ((scaled_state - num) % scaled_LR) // scaled_L
				else: grundy ^= (scaled_state % scaled_LR) // scaled_L

			if grundy == 0:
				return str(pile), str(round(num / PRECISION, 3))

	assert(False)

def getInput():
	pile = ""
	num  = ""

	if turn == 1:
		pile, num = getBotInput()
		print(f"Bot chose pile: {pile}")
		print(f"Bot took away: {num}")
	else:
		pile = input("Choose the pile you want to take from (0-index): ")
		num  = input("Choose the amount you want to take (within the bounds): ")

	return pile, num

while not isGameEnd:
	pile, num = getInput()

	try:
		pile = int(pile)
		num = round(float(num), 3)

		if num < L or num > R:
			print(f"Input between {L} and {R}!")
			continue

		if state[pile] < num:
			print("That pile doesn't have this much :(")
			continue
	except:
		print("INVALID INPUT!")
		continue

	print()

	state[pile] -= num
	state[pile] = round(state[pile], 3)

	if all(x == 0 or x < L for x in state):
		isGameEnd = True
		if turn == 0:
			print(f"You beat the bot! Here's da flag: {FLAG}")
		else:
			print("Bro can't even beat a computer. #AItakeovertheworld")

	turn ^= 1
