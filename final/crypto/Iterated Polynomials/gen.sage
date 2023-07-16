p = 2^32+15
R = GF(p)[x]
a = R(x)^16+R.random_element(degree=15)
S.<y> = R.quotient(a)
M = Matrix([list((y^2+1)^n) for n in range(16)])
while [i[0].degree() for i in factor(M.charpoly())]!=[1,2,3,4,6]:
    print([i[0].degree() for i in factor(M.charpoly())])
    a = R(x)^16+R.random_element(degree=15)
    S.<y> = R.quotient(a)
    M = Matrix([list((y^2+1)^n) for n in range(16)])
g = y
s = int("7h3_FunC710N_15_4c7U4Lly_l1N34r!".encode().hex(),16)
v = vector(GF(p),[0]*16)
v[1]=1
g = sum(i*y^n for n,i in enumerate(v*M^s))
print(f"{p = }")
print(f"{a = }")
print(f"{g = }")
