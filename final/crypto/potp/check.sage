import secrets
import random

mod = 2^14

x1 = secrets.randbelow(int(2**8))
x2 = secrets.randbelow(int(2**8))

m = random.randint(20,126)
c1 = secrets.randbelow(int(2**8))
c2 = secrets.randbelow(int(2**8))

print(m)

divisorsList = {}
divideList = {}

for i in range(2**9):
    for j in range(i + 1, 2**9):
        k = (i * j) % mod
        
        if k not in divisorsList:
            divisorsList[k] = []

        if i not in divisorsList[k]:
            divisorsList[k].append(i)
        if j not in divisorsList[k]:
            divisorsList[k].append(j)
        
        if (k, j) not in divideList:
            divideList[(k,j)] = []

        if (k, i) not in divideList:
            divideList[(k,i)] = []

        if j not in divideList[(k,i)]:
            divideList[(k,i)].append(j)
        if i not in divideList[(k,j)]:
            divideList[(k,j)].append(i)


k1 = Zmod(mod)(x1 * m + x2 * m)
k2 = Zmod(mod)(x1 * c1)
k3 = Zmod(mod)(x2 * c2)


for i in divisorsList[k2]:
    ok = False
    for t in divideList[(k2,i)]:
        if (t <= 2**8):
            ok = True
            break
    if (i >= 2**8 or not ok):
        continue
    for j in divisorsList[k3]:
        ok = False
        for t in divideList[(k3,j)]:
            if (t <= 2**8):
                ok = True
                break
        if (j >= 2**8 or not ok):
            continue

        k = (i + j) % mod
        if ((k1,k) not in divideList):
            continue
        for z in divideList[(k1,k)]:
            if (20 <= z <= 127):
                print(z)