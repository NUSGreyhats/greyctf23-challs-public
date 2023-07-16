mod = 2^13

F.<x> = Zmod(mod)[]

def poly_to_bytes(s):
    l = s.coefficients()
    res = ''
    for i in l:
        res += chr(i)
    return res

c1 = 491*x^126 + 5268*x^125 + 771*x^124 + 890*x^123 + 4024*x^122 + 7391*x^121 + 3590*x^120 + 2674*x^119 + 111*x^118 + 7817*x^117 + 6268*x^116 + 5653*x^115 + 7670*x^114 + 3655*x^113 + 1089*x^112 + 6273*x^111 + 5160*x^110 + 5060*x^109 + 3763*x^108 + 3620*x^107 + 2338*x^106 + 6273*x^105 + 6775*x^104 + 6846*x^103 + 1858*x^102 + 6694*x^101 + 8177*x^100 + 3416*x^99 + 1909*x^98 + 1622*x^97 + 7381*x^96 + 7834*x^95 + 6464*x^94 + 5063*x^93 + 2805*x^92 + 4230*x^91 + 7883*x^90 + 3346*x^89 + 4100*x^88 + 832*x^87 + 5107*x^86 + 502*x^85 + 7720*x^84 + 2352*x^83 + 3470*x^82 + 3100*x^81 + 6762*x^80 + 3256*x^79 + 7799*x^78 + 795*x^77 + 3928*x^76 + 7325*x^75 + 7747*x^74 + 3480*x^73 + 6675*x^72 + 6678*x^71 + 4996*x^70 + 2948*x^69 + 822*x^68 + 2997*x^67 + 1621*x^66 + 3023*x^65 + 5612*x^64 + 7353*x^63 + 1765*x^62 + 5443*x^61 + 1833*x^60 + 6925*x^59 + 7112*x^58 + 7141*x^57 + 2964*x^56 + 8086*x^55 + 1423*x^54 + 1786*x^53 + 6053*x^52 + 6808*x^51 + 3524*x^50 + 6585*x^49 + 2962*x^48 + 3761*x^47 + 6192*x^46 + 7762*x^45 + 6530*x^44 + 601*x^43 + 7095*x^42 + 1012*x^41 + 3688*x^40 + 2057*x^39 + 1598*x^38 + 2058*x^37 + 6615*x^36 + 7527*x^35 + 4087*x^34 + 7888*x^33 + 2405*x^32 + 6291*x^31 + 6871*x^30 + 3274*x^29 + 4438*x^28 + 5637*x^27 + 3565*x^26 + 3629*x^25 + 991*x^24 + 6909*x^23 + 4277*x^22 + 8145*x^21 + 1579*x^20 + 6905*x^19 + 5654*x^18 + 1040*x^17 + 812*x^16 + 6387*x^15 + 6116*x^14 + 6317*x^13 + 2423*x^12 + 5768*x^11 + 1166*x^10 + 2450*x^9 + 2673*x^8 + 1892*x^7 + 4923*x^6 + 3698*x^5 + 1459*x^4 + 7995*x^3 + 1397*x^2 + 2480*x + 1325
c2 = 1440*x^126 + 6960*x^125 + 7242*x^124 + 2354*x^123 + 1897*x^122 + 3700*x^121 + 145*x^120 + 533*x^119 + 148*x^118 + 8189*x^117 + 7483*x^116 + 5417*x^115 + 3765*x^114 + 2343*x^113 + 6418*x^112 + 1110*x^111 + 7701*x^110 + 3571*x^109 + 3696*x^108 + 2976*x^107 + 5453*x^106 + 2398*x^105 + 5314*x^104 + 5965*x^103 + 6432*x^102 + 1752*x^101 + 3772*x^100 + 3718*x^99 + 364*x^98 + 4747*x^97 + 4096*x^96 + 4006*x^95 + 4440*x^94 + 6972*x^93 + 6676*x^92 + 6511*x^91 + 6697*x^90 + 2079*x^89 + 337*x^88 + 2577*x^87 + 6260*x^86 + 6681*x^85 + 82*x^84 + 5284*x^83 + 2808*x^82 + 4340*x^81 + 2310*x^80 + 725*x^79 + 7162*x^78 + 6827*x^77 + 1423*x^76 + 1774*x^75 + 5432*x^74 + 4007*x^73 + 4465*x^72 + 7189*x^71 + 5214*x^70 + 1029*x^69 + 5488*x^68 + 5378*x^67 + 1508*x^66 + 371*x^65 + 6794*x^64 + 8058*x^63 + 1709*x^62 + 5117*x^61 + 2648*x^60 + 7454*x^59 + 6564*x^58 + 6857*x^57 + 2939*x^56 + 5389*x^55 + 6116*x^54 + 7083*x^53 + 2386*x^52 + 6451*x^51 + 6757*x^50 + 2338*x^49 + 6426*x^48 + 7972*x^47 + 2480*x^46 + 3492*x^45 + 5611*x^44 + 3443*x^43 + 5657*x^42 + 7622*x^41 + 7750*x^40 + 3471*x^39 + 6641*x^38 + 5168*x^37 + 5733*x^36 + 5862*x^35 + 2375*x^34 + 3200*x^33 + 6468*x^32 + 5536*x^31 + 5886*x^30 + 2240*x^29 + 7933*x^28 + 4133*x^27 + 4933*x^26 + 413*x^25 + 2339*x^24 + 3716*x^23 + 1561*x^22 + 715*x^21 + 1654*x^20 + 3955*x^19 + 1291*x^18 + 1471*x^17 + 6497*x^16 + 957*x^15 + 7954*x^14 + 4301*x^13 + 4382*x^12 + 4479*x^11 + 2475*x^10 + 4586*x^9 + 2745*x^8 + 6356*x^7 + 7280*x^6 + 5328*x^5 + 2865*x^4 + 6069*x^3 + 1091*x^2 + 646*x + 2768
c3 = 3444*x^126 + 7293*x^125 + 7131*x^124 + 607*x^123 + 2807*x^122 + 763*x^121 + 5862*x^120 + 1099*x^119 + 4943*x^118 + 4910*x^117 + 5771*x^116 + 6051*x^115 + 7707*x^114 + 2259*x^113 + 5773*x^112 + 2888*x^111 + 882*x^110 + 7368*x^109 + 344*x^108 + 2415*x^107 + 5084*x^106 + 552*x^105 + 6203*x^104 + 353*x^103 + 328*x^102 + 2538*x^101 + 3063*x^100 + 2003*x^99 + 919*x^98 + 7696*x^97 + 5355*x^96 + 4794*x^95 + 1865*x^94 + 7717*x^93 + 7950*x^92 + 6656*x^91 + 7748*x^90 + 3092*x^89 + 5061*x^88 + 8151*x^87 + 3593*x^86 + 4580*x^85 + 4552*x^84 + 3751*x^83 + 2338*x^82 + 2282*x^81 + 273*x^80 + 1295*x^79 + 4470*x^78 + 5706*x^77 + 6575*x^76 + 4783*x^75 + 4676*x^74 + 2132*x^73 + 5191*x^72 + 2759*x^71 + 5266*x^70 + 4542*x^69 + 8061*x^68 + 7059*x^67 + 7210*x^66 + 3122*x^65 + 5348*x^64 + 1932*x^63 + 6409*x^62 + 7254*x^61 + 6542*x^60 + 5696*x^59 + 4297*x^58 + 3304*x^57 + 1080*x^56 + 5881*x^55 + 8113*x^54 + 6433*x^53 + 7621*x^52 + 4427*x^51 + 1041*x^50 + 3506*x^49 + 1936*x^48 + 5673*x^47 + 3138*x^46 + 1073*x^45 + 1142*x^44 + 4056*x^43 + 7169*x^42 + 354*x^41 + 1869*x^40 + 388*x^39 + 6288*x^38 + 6463*x^37 + 2914*x^36 + 7423*x^35 + 7373*x^34 + 5813*x^33 + 4374*x^32 + 3640*x^31 + 5802*x^30 + 313*x^29 + 2572*x^28 + 3620*x^27 + 193*x^26 + 208*x^25 + 671*x^24 + 5330*x^23 + 2488*x^22 + 2621*x^21 + 1272*x^20 + 6633*x^19 + 4674*x^18 + 7660*x^17 + 3149*x^16 + 5217*x^15 + 1556*x^14 + 5422*x^13 + 7502*x^12 + 5472*x^11 + 1332*x^10 + 3170*x^9 + 7800*x^8 + 6964*x^7 + 5202*x^6 + 6913*x^5 + 2380*x^4 + 1731*x^3 + 3230*x^2 + 3944*x + 7808

divisorsList = {}
divideList = {}

for i in range(2**9):
    for j in range(i, 2**9):
        k = (i * j) % mod
        
        if k not in divisorsList:
            divisorsList[k] = []

        if i not in divisorsList[k]:
            divisorsList[k].append(i)
        if j not in divisorsList[k]:
            divisorsList[k].append(j)
        
        if (k, j) not in divideList:
            divideList[(k,j)] = []

        if (k, i) not in divideList:
            divideList[(k,i)] = []

        if j not in divideList[(k,i)]:
            divideList[(k,i)].append(j)
        if i not in divideList[(k,j)]:
            divideList[(k,j)].append(i)

c1l = c1.coefficients()
c2l = c2.coefficients()
c3l = c3.coefficients()
n = len(c1l)

def func(t1, t2, t3, o1, o2, o3):
    deg = len(t1)
    print("".join(map(lambda x : chr(x), t1)))
    if (chr(t1[-1]) == '}'):
        return

    first = c1l[deg]
    second = c2l[deg]
    third = c3l[deg]
    for i in range(1, deg):
        first -= t1[deg - i] * o1[i]
        second -= t2[deg - i] * o2[i]
        third -= t3[deg - i] * o3[i]

    first %= mod
    second %= mod
    third %= mod
    
    for i in range(2**8):
        k2 = (second - i * t2[0]) % mod
        if (k2 not in divisorsList): continue
        if ((k2, o2[0]) not in divideList): continue
        ok = False
        for check in divideList[(k2, o2[0])]:
            if (20 <= check <= 127): ok = True; break
        if (not ok): continue
        for j in range(2**8):
            k3 = (third - j * t3[0]) % mod
            if (k3 not in divisorsList): continue
            if ((k3, o3[0]) not in divideList): continue
            ok = False
            for check in divideList[(k3, o3[0])]:
                if (20 <= check <= 127): ok = True; break
            if (not ok): continue

            k = (i + j) % mod
            k1 = (first - t1[0] * k) % mod
            if ((k1, o1[0]) not in divideList): continue
            for tt1 in divideList[(k1, o1[0])]:
                if (20 <= tt1 <= 127):
                    for tt2 in divideList[(k2, o2[0])]:
                        if (20 <= tt2 <= 127):
                            for tt3 in divideList[(k3, o3[0])]:
                                if (20 <= tt3 <= 127):
                                    func(t1 + [tt1], t2 + [tt2], t3 + [tt3], o1 + [k], o2 + [i], o3 + [j])

k1 = c1l[0]
k2 = c2l[0]
k3 = c3l[0]
for i in divisorsList[k2]:
    ok = False
    for t in divideList[(k2,i)]:
        if (20 <= t <= 127): ok = True; break
    if (i >= 2**8 or not ok): continue

    for j in divisorsList[k3]:
        ok = False
        for t in divideList[(k3,j)]:
            if (20 <= t <= 127): ok = True; break
        if (j >= 2**8 or not ok): continue
        
        k = (i + j) % mod
        if ((k1,k) not in divideList): continue
        for z in divideList[(k1,k)]:
            if (20 <= z <= 127):
                for tt2 in divideList[(k2,i)]:
                    if (20 <= tt2 <= 127): 
                        for tt3 in divideList[(k3, j)]:
                            if (20 <= tt3 <= 127):
                                func([z],[tt2],[tt3],[k],[i],[j])

