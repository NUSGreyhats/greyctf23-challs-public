import pulp

from secrets import randbelow

M = [[randbelow(25) * (-1)**randbelow(2) for j in range(128)] for i in range(128)]

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

print("Optimal strategy for player")

player = []

for i in vars:
    player.append(pulp.value(i))

print(player)

print("Player Profit = ", pulp.value(Lp_prob.objective))

## Server

MT = [[-M[j][i] for j in range(128)] for i in range(128)]

Lp_prob = pulp.LpProblem('GameServer', pulp.LpMaximize)

v = pulp.LpVariable(f"v")

vars = [pulp.LpVariable(f"x{i}", lowBound=0) for i in range(128)]

Lp_prob += v

for i in range(128):
    f = 0
    for j in range(128):
        f += vars[j] * MT[j][i]
    Lp_prob += v <= f

Lp_prob += sum(vars) == 1

Lp_prob.solve()

print("Optimal strategy for server")

server = []

for i in vars:
    server.append(pulp.value(i))

print(server)

print("Server Profit = ", pulp.value(Lp_prob.objective))

