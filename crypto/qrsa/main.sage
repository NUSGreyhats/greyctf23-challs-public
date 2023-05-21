from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes, getPrime
from decimal import Decimal, getcontext
import secrets

FLAG = b'grey{x3VkGD3K2SK5s4JW_Lmao_why_do_RSA_in_quadratic_integer}'

getcontext().prec = int(10000)

class Q:
    d = 41
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __add__(self, other):
        return Q(self.a + other.a, self.b + other.b)
    
    def __sub__(self, other):
        return Q(self.a - other.a, self.b - other.b)
    
    def __mul__(self, other):
        a = self.a * other.a + Q.d * self.b * other.b
        b = self.b * other.a + self.a * other.b 
        return Q(a, b)

    def __mod__(self, other):
        r = Decimal(int(other.a * other.a - Q.d * other.b * other.b))
        q = self * Q(other.a, -other.b)
        qa = int((Decimal(int(q.a))/r).to_integral_exact())
        qb = int((Decimal(int(q.b))/r).to_integral_exact())
        res = self - Q(qa, qb) * other
        return res
    
    def __str__(self) -> str:
        return f'({self.a}, {self.b})'
    
def power(a, b, m):
    res = Q(1, 0)
    while (b > 0):
        if (b & 1): res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

n = len(FLAG)

p = Q(1, 0)
q = Q(1, 0)

for i in range(10):
    p *= Q(secrets.randbits(32), 0) * Q(getPrime(40), getPrime(40))
    q *= Q(0, secrets.randbits(32)) * Q(getPrime(40), getPrime(40))

N = p * q
m = Q(bytes_to_long(FLAG[:n//2]), bytes_to_long(FLAG[n//2:]))

e = 0x10001
c = power(m, e, N)

f = factor(N.a * N.a - Q.d * N.b * N.b)
print(f)

ord = 1
ord2 = 1

for i in f:
    ord *= (i[0] - 1)**2 * (i[0]**2 - 1) * i[0]**i[1] 
    ord2 *= (i[0] - 1) * i[0]**(i[1] - 1)

d = int(inverse(e, ord))
d2 = int(inverse(e, ord2))

k = power(m, ord, N)
k2 = power(m, ord2, N)
m1 = power(c, d, N)
m2 = power(c, d2, N)

print(k)
print(k2)
print(N)
print(c)
print(long_to_bytes(m1.a) + long_to_bytes(m1.b))
print(long_to_bytes(m2.a) + long_to_bytes(m2.b))