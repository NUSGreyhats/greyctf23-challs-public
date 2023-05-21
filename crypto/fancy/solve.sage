from hashlib import shake_256

def xor(a, b):
    return bytes([i ^^ j for i, j in zip(a,b)])

def decrypt(s, c):
    secret = b",".join(map(lambda x : str(x).encode(), s.coefficients()))
    key = shake_256(secret).digest(len(c))
    return xor(key, c)

p = 2^29 - 33

d1 = 3
d2 = 7

pari.allocatemem(42949672960)

F = PolynomialRing(GF(p), 'a', d1 * d2 + 2)

variables = F.gens()
x = variables[0]
y = variables[1]

G = F.quotient(F.ideal([x^d1 - y^2 + 1, y^d2 - 11]))

variables = G.gens()
x = variables[0]
y = variables[1]

g = 1 + x + y

c = bytes.fromhex("cd519d06bf85ecafdb84111ab63d509e49ffb8cfc78fee4f4cbc3c007a96d2060613f5c0a208325569bf3476d4ea839c10d4667d3dfb5d0d650d79153b")
A = -210623603*x^2*y^6 + 223917991*x^2*y^5 - 234939507*x*y^6 - 103510738*x^2*y^4 - 255193765*x*y^5 + 245323126*y^6 - 41129482*x^2*y^3 + 3293396*x*y^4 + 265040169*y^5 - 175348566*x^2*y^2 - 8922481*x*y^3 - 76227659*y^4 - 127516194*x^2*y - 97886874*x*y^2 - 207888821*y^3 - 123290485*x^2 + 93703664*x*y - 146824287*y^2 - 229640558*x - 5428142*y - 185137098
B = 155912203*x^2*y^6 - 50064221*x^2*y^5 + 107681922*x*y^6 - 249464027*x^2*y^4 - 13560651*x*y^5 - 178499062*y^6 + 75225430*x^2*y^3 + 241399622*x*y^4 + 8431316*y^5 - 15433512*x^2*y^2 - 80127041*x*y^3 - 199374666*y^4 + 203619258*x^2*y + 20681482*x*y^2 - 92775952*y^3 - 46663623*x^2 + 171776018*x*y - 164809964*y^2 - 186955302*x + 235677332*y - 173567532

f = 0
for i in range(d1):
    for j in range(d2):
        f += variables[2 + d2 * i + j] * x^i * y^j

def hom(k):
    M = [[0 for _ in range(d1 * d2)] for _ in range(d1 * d2)]
    t = (f * k).lift()
    for i in range(d1):
        for j in range(d2):
            for k in range(d1 * d2):
                M[k][d2 * i + j] = t.coefficient({x:i, y: j, variables[2 + k]: 1})
    return Matrix(GF(p), M)
            
G = hom(g)
AA = hom(A)
print(p)
print(G)
gg = G.charpoly()
n = len(G.rows())

factors = factor(gg)

val = []
mods = []

order = 1

for f in factors:
    print(f)
    FF = GF(p ^ f[0].degree())
    root = f[0].change_ring(FF).roots()[0][0]
    v = (G.change_ring(FF) - root * 1).right_kernel_matrix().rows()[0]
    P = [v] + [[1 if i == j else 0 for j in range(n)] for i in range(n - 1)]
    P = Matrix(FF, P).transpose()
    T1 = P^-1 * G.change_ring(FF) * P
    T2 = P^-1 * AA.change_ring(FF) * P
    o = T1[0][0].multiplicative_order()
    if (lcm(order, o) == order):
        continue 
    order = lcm(order, o)
    val.append(T2[0][0].log(T1[0][0]))
    mods.append(T1[0][0].multiplicative_order())

a = crt(val, mods)

print(order)

s = (B^a).lift()
print(s)
print(decrypt(s, c))

