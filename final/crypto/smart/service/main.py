#!/usr/local/bin/python

from secrets import randbits

FLAG = 'grey{hello_smart_admin_;D_hRkPxgxcMB7Yxk4e}'

p = 1657; q = 1663; r = 1049; s = 1193

def f(v):
    a = (5 * v[0] + 3 * v[1] + 7 * v[2] + 4 * v[3] + v[0] * v[1] + 10 * (v[2] * v[3])**2) % p
    b = (9 * v[0] + 2 * v[1] + 1 * v[2] + 1 * v[3] + v[1] * v[2] + 11 * (v[0] * v[3])**2) % q
    c = (6 * v[0] + 7 * v[1] + 3 * v[2] + 9 * v[3] + v[2] * v[3] + 12 * (v[0] * v[1])**2) % r
    d = (8 * v[0] + 5 * v[1] + 2 * v[2] + 7 * v[3] + v[3] * v[0] + 13 * (v[1] * v[2])**2) % s
    return (a,b,c,d)

def h(v):
    k = 5555 + ((v[0] * v[1] * v[2] * v[3]) % 3000000)
    for _ in range(k):
        v = f(v)
    return v

def checkInput(v):
    if (len(v) != 4):
        return False
    return 0 <= v[0] < p and 0 <= v[1] < q and 0 <= v[2] < r and 0 <= v[3] < s
    
def check(v1, v2):
    if (len(v1) != len(v2)): 
        return False
    for i in range(len(v1)):
        if (v1[i] != v2[i]):
            return False
    return True

print("Our admins are smart. Prove your intelligence to gain access")

secret = [randbits(32) for _ in range(4)]
target = h(secret)

print("Target:", target)

print("Insert the secret key (4 integers separated by comma)")
token = list(map(int, input().split(',')))

if (not checkInput(token)):
    print("Input bad x.x")
    exit(0)

if (check(h(token), target)):
    print("Welcome admin!", FLAG)
else:
    print("Wrong, bye")
    