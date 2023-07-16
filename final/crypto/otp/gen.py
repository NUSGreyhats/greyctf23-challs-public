from secrets import randbelow
from Crypto.Util.number import getPrime

print([-randbelow(2**32) if randbelow(2) == 0 else randbelow(2**32) for _ in range(10)])
print(getPrime(1024))