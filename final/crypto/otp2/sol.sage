from pwn import *
from secrets import randbits

n = 6
while True:
    r = remote("34.124.157.94", 19622)

    r.recvuntil("p: ")
    p = int(r.recvline().decode())
    factors = {}
    # Partial factorisation
    k = p-1

    for i in range(13):
        for _ in range(5):
            f = ecm.one_curve(k, factor_digits=i)
            k = k//f[0]
            if (f[0] != 1):        
                for t in factor(f[0]):
                    if t not in factors:
                        factors[t[0]] = 0
                    factors[t[0]] += t[1]

    print(factors)

    temp = []
    for f in factors: 
        if (f <= 2**5): continue
        if (f >= 2**40): continue
        if (factors[f] == 1):
            temp.append(f)

    factors = temp
    factors.sort()

    print(factors)
    k = 1
    for i in factors:
        k *= i
    
    print(int(k).bit_length())

    if (k >= 2^110):
        break
    r.close()

r.recvuntil("pub: [")
pub = list(map(int, r.recvline().decode()[:-2].split(',')))

y = [randbits(90) for _ in range(n)]

payload = ''
for i in range(n):
    payload += str(y[i]) + ','

payload = payload[:-1]
r.sendline(payload)

r.recvuntil("Token Hash: ")
skey = int(r.recvline().decode())

r.recvuntil("OTP Hash: [")
ct = list(map(int, r.recvline().decode()[:-2].split(',')))

A = GF(p)(1)

for i in range(1, len(ct)):
    A *= pow(ct[i], y[i - 1], p)

A = A / pow(ct[0], skey, p)

g = GF(p)((5 * 7)^10)

vals = []
        
for f in factors:
    vals.append(discrete_log(A ^ ((p-1)//f), g ^ ((p-1)//f), f))

s = crt(vals, factors)

print(s)

X = 2^100

M = [
    [1, 0, 0, 0, 0, 0, X * y[0], 0],
    [0, 1, 0, 0, 0, 0, X * y[1], 0],
    [0, 0, 1, 0, 0, 0, X * y[2], 0],
    [0, 0, 0, 1, 0, 0, X * y[3], 0],
    [0, 0, 0, 0, 1, 0, X * y[4], 0],
    [0, 0, 0, 0, 0, 1, X * y[5], 0],
    [0, 0, 0, 0, 0, 0, -X * s, 2^16]
]

M = Matrix(ZZ, M).LLL()

print(M)

row = 0

for i in range(6):
    if (M[i][-1] != 0):
        row = i
        break

payload = ''
for i in range(6):
    payload += str(M[row][i]) + ','

payload = payload[:-1]
r.sendline(payload)

r.interactive()