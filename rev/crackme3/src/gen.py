import random

random.seed(6110)

# for i in range(64):
#     print(f"us f{i+1}(us, us);")

ADDS = []
SUBS = []

print("us f9(us x, us y) { return x + y; }")
for i in range(23):
    ADDS.append(random.randint(1, 0xffff))
    print(f"us f{10+i}(us x, us y) {{ return (x + y) ^ {ADDS[-1]:#x}; }}")

print("us f33(us x, us y) { return x - y; }")
for i in range(23):
    SUBS.append(random.randint(1, 0xffff))
    print(f"us f{34+i}(us x, us y) {{ return (x - y) ^ {SUBS[-1]:#x}; }}")

for i in range(8):
    print(f"us f{57+i}(us x, us y) {{ return {random.randint(1, 0xffff):#x}; }}")

print(ADDS)
print(SUBS)

print("OF O[64] = {")
fs = [f"&f{i+1}" for i in range(64)]
print(f"    {','.join(fs)}")
print("};")

routs = [f"&R[{i}]" for i in range(64)]
print(f"us* ROUT[64] = {{ {', '.join(routs)} }};")

rins = [f"&R[{i}]" for i in range(64)]
print(f"us* RIN[64] = {{ {', '.join(rins)} }};")

rins = [f"&O[{i}]" for i in range(64)]
print(f"OFP* OOUT[64] = {{ {', '.join(rins)} }};")