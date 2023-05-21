from Crypto.Util.number import getPrime

p = 2^29 - 33

F.<x,y> = GF(p)[]
G.<x,y> = F.quotient(F.ideal([x^3 - y^2 + 1, y^7 - 11]))

g = 1 + x + y

for i in range(1, 23):
    k = g^(p^i - 1)
    if (k== 1):
        print(p^i - 1)
        print(i)
    

