import random
from datetime import datetime
random.seed(datetime.now().timestamp())

turn = 0
isGameEnd = False

FLAG = "REDACTED"

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

def getBotInput():
	# Super secret AI stuff (probably)
	return "", ""

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
