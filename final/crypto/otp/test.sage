from secrets import randbelow

x = [randbelow(int(2^16)) for _ in range(10)]
y1 = [randbelow(int(2^100)) for _ in range(10)]
s1 = 0
s2 = 0

for i in range(6):
    s1 += x[i] * y1[i]

print(x)

M = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, y1[0], 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, y1[1], 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, y1[2], 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, y1[3], 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, y1[4], 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, y1[5], 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, s1, 2^16]
]

M = Matrix(M)

print(M.LLL())