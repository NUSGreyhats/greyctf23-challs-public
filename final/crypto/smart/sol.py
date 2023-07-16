from pwn import *

p = 1657; q = 1663; r = 1049; s = 1193

def f(v):
    a = (5 * v[0] + 3 * v[1] + 7 * v[2] + 4 * v[3] + v[0] * v[1] + 10 * (v[2] * v[3])**2) % p
    b = (9 * v[0] + 2 * v[1] + 1 * v[2] + 1 * v[3] + v[1] * v[2] + 11 * (v[0] * v[3])**2) % q
    c = (6 * v[0] + 7 * v[1] + 3 * v[2] + 9 * v[3] + v[2] * v[3] + 12 * (v[0] * v[1])**2) % r
    d = (8 * v[0] + 5 * v[1] + 2 * v[2] + 7 * v[3] + v[3] * v[0] + 13 * (v[1] * v[2])**2) % s
    return (a,b,c,d)

def check(v1, v2):
    if (len(v1) != len(v2)): 
        return False
    for i in range(len(v1)):
        if (v1[i] != v2[i]):
            return False
    return True

while True:
    rr = remote("localhost", 9999)

    rr.recvuntil("Target: (")
    target = list(map(int, rr.recvline().decode()[:-2].split(",")))
    v = target

    count = 0

    for _ in range(3000000):
        v = f(v)
        count += 1
        if (check(v, target)):
            break
    else:
        rr.close()
        continue

    print(count)

    v = target
    for i in range(count):
        if (5555 + ((v[0] * v[1] * v[2] * v[3]) % 3000000) + i) == count:
            print("Found!")
            rr.sendline(f"{v[0]}, {v[1]}, {v[2]}, {v[3]}")
            rr.interactive()
            exit(0)
        v = f(v)

    rr.close()

