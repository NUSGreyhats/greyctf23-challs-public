p = 4294967311
R = GF(p)[x]
a = x^16 + 2206327570*x^15 + 764008823*x^14 + 2624308288*x^13 + 584210452*x^12 + 2859245580*x^11 + 2161247258*x^10 + 2475621239*x^9 + 2679079*x^8 + 3262843933*x^7 + 3126742286*x^6 + 2840770970*x^5 + 2798946498*x^4 + 1178619281*x^3 + 124682568*x^2 + 150251198*x + 1469826103
S.<y> = R.quotient(a)
g = y
h = 4213081404*y^15 + 3296429821*y^14 + 4211675621*y^13 + 1980847685*y^12 + 1112259653*y^11 + 330484598*y^10 + 23881381*y^9 + 2112413024*y^8 + 2815876074*y^7 + 4197415602*y^6 + 3078141258*y^5 + 4163495398*y^4 + 4121679949*y^3 + 2775737979*y^2 + 1590517927*y + 1223073206
M = Matrix([list((y^2+1)^n) for n in range(16)])
F = GF(p)[x]
a = F(x)^2
while a.is_irreducible()==False:
    a = F.random_element(degree=12)
F.<z> = GF(p^12,modulus=a)

M = M.change_ring(F)
g = vector(F,list(g))
h = vector(F,list(h))
D,P=M.eigenmatrix_left()
c=[]
m=[]
for i in range(1,16):
    t = D[i,i].multiplicative_order()
    if t in m:
        continue
    m.append(t)
    c.append(((h*P^-1)[i]/(g*P^-1)[i]).log(D[i,i]))
    print(c[-1],m[-1])
print("grey{"+bytes.fromhex(hex(crt(c,m))[2:]).decode()+"}")
