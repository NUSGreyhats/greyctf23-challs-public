import secrets
from random import randint

FLAG = <REDACTED>

F.<x> = Zmod(2^13)[]

def bytes_to_poly(s):
    res = 0
    for i in range(len(s)):
        res += x^i * s[i]
    return res

def genOtp(n):
    return bytes_to_poly(secrets.token_bytes(n))

n = len(FLAG)

otp2 = genOtp(n)
otp3 = genOtp(n) 
otp1 = otp2 + otp3

m2 = bytes_to_poly(bytes([randint(20, 127) for _ in range(n)]))
m3 = bytes_to_poly(bytes([randint(20, 127) for _ in range(n)]))
m1 = bytes_to_poly(FLAG)

print(m1 * otp1)
print(m2 * otp2)
print(m3 * otp3)
