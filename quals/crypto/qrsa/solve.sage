from Crypto.Util.number import inverse, long_to_bytes
from decimal import Decimal, getcontext

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

N_a = 2613240571441392195964088630982261349682821645613497396226742971850092862049682714123355029612448609254303796690909646594946069650719320421550307082460305103785198772732273571020529003974320397237096691522804712706512030715753640155668659684093067319185265153545236392472134496428382266600090383797614653942221936332929175557303391656241351117808833959918253404012245633586322491783496235954011173498460231177697737092488315432823871012224368640000000
N_b = 406631291381063062708368640624433195177629887128324992156536215422427085251271158548246052765619573442134462500652616281986273622217404519958464200902599497611719198311591180368508835389781999428982410097278062504076636059232055783729252448502542597951710294264137195997893054083787667027206495381119048279226753306334118272352371363733528942151156768581101905518532465160584386180402709606771189313858666352673319676040954150310530906188677120000000
C_a = 2548711194583905242838482900078294859199882484375229964715550469790767416706725411953362845724983002558821710679258499982960453598798074631796750663774845415692650589352513765870894878170769435087683220330986573614974529690187792931316475879984809267941606365493481277785184076320720487644565808909403821593150101568803446075808715002632463329841749179295823686361086890490703942659897558782785569910876849941888829825694107185482012864247559426111336
C_b = 400941158148299866665115436146084555297152646914223433988293961893848206718639579342053294961462797881591789534709492717097892667288044693824228320005182068933966525404665323301134912609777110824069569544060608441451336249895977866445507357131208911196230972379132737483251711155975474018188763433151191428844929401881703566513896999328525340678378000286116960582957867857836600614501387296599091266404311307529322130111164410987643652390537358307965
e = 65537

N = Q(N_a, N_b)
c = Q(C_a, C_b)

f = factor(N.a * N.a - Q.d * N.b * N.b)
print(f)

ord = 1
ord2 = 1

for i in f:
    ord *= (i[0] - 1)**2 * (i[0]**2 - 1) * i[0]**i[1] 
    ord2 *= (i[0] - 1) * i[0]**(i[1] - 1)

d = int(inverse(e, ord))
d2 = int(inverse(e, ord2))

m1 = power(c, d, N)
m2 = power(c, d2, N)

print(N)
print(c)
print(long_to_bytes(m1.a) + long_to_bytes(m1.b))
print(long_to_bytes(m2.a) + long_to_bytes(m2.b))