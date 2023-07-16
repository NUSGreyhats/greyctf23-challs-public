from pwn import *
import pulp
from random import choice, uniform

def choose_rand(arr):
    t = uniform(0, 1)
    for tt in range(len(arr)):
        if (t <= arr[tt]):
            return tt
        t -= arr[tt]
    return len(arr) - 1

while True:
    r = remote("localhost", 9999)

    r.recvuntil(b"payoff = [")

    M = []
    for _ in range(128):
        r.recvuntil(b"[")
        row = list(map(int, r.recvuntil(b"]")[:-1].split(b",")))
        M.append(row)

    Lp_prob = pulp.LpProblem('Game', pulp.LpMaximize)

    v = pulp.LpVariable(f"v")

    vars = [pulp.LpVariable(f"x{i}", lowBound=0) for i in range(128)]

    Lp_prob += v

    for i in range(128):
        f = 0
        for j in range(128):
            f += vars[j] * M[j][i]
        Lp_prob += v <= f

    Lp_prob += sum(vars) == 1

    Lp_prob.solve()

    print(pulp.value(Lp_prob.objective))
    if not (pulp.value(Lp_prob.objective) >= 0.5):
        r.close()
        continue

    player = []

    for i in range(128):
        player.append(pulp.value(vars[i]))

    # Strategy maximum

    # maxi = -1000
    # k = 0
    # for i in range(128):
    #     if (maxi <= sum(M[i])):
    #         maxi = sum(M[i])
    #         k = i

    # player2 = [k]

    # Strategy uniform
    
    #player2 = [i for i in range(128)]

    r.recvuntil("Note:")

    for i in range(10000):
        r.sendline(str(choose_rand(player)))
        # r.sendline(str(choice(player2)))
        r.recvuntil("$")
        money = int(r.recvuntil(" ").decode())
        print(i, money)
        if (money <= 0): break
        if (money >= 10000): break


    print("Player Profit = ", pulp.value(Lp_prob.objective))

    if (money >= 10000):
        r.interactive()
    else:
        r.close()

