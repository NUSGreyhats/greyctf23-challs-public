from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from pwn import *

def decrypt(msg, key):
    cipher = AES.new(pad(key, 16), AES.MODE_CTR, nonce=b'\xc1\xc7\xcc\xd1D\xfbI\x10')
    return cipher.decrypt(msg)

while True:
    r = remote("localhost", 9999)
    r.recvuntil("our lucky numbers\n")
    sample = list(map(int, r.recvline().decode().strip().split()))

    trans = [[0 for _ in range(2**8)] for _ in range(2**8)]

    for i in sample:
        for j in sample:
            for k in range(2**8):
                trans[k][(j * k + i) % 256] += (1)/(len(sample)^2)

    for i in range(2**8):
        trans[i][i] -= 1
        trans[i].append(1)

    T = Matrix(QQ, trans)

    T = T.transpose()

    v = list(T.solve_right(vector([0 for _ in range(256)] + [1])))
    for i in range(len(v)):
        v[i] = (v[i], i)

    v.sort(key=lambda x : x[0])

    # for i in range(len(v)):
    #     print(v[i][0].n(50), v[i][1])

    k = sum(map(lambda x : x[0], v[-12:])).n(50)

    print(sample)
    print(k)
    if (k < 0.4):
        r.close()
        continue

    arr = list(map(lambda x : x[1], v[-12:]))

    
    print(arr)

    r.sendline("10")

    for _ in range(10):
        r.recvuntil("lucky flag: ")
        c = bytes.fromhex(r.recvline().decode())

        for i in range(12**6):
            key = []
            for _ in range(6):
                key.append(int(arr[i % 12]))
                i = i // 12
            key = bytes(key)
            if b'grey{' in decrypt(c, key):
                print(decrypt(c, key))
                exit(0)
    r.close()

