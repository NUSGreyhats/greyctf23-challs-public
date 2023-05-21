from pwn import p8, p16, p32, p64
import random

random.seed(116)

flag = "grey{r_y0u_d1zzy?_9bfad}"

OP_IDXS = [i for i in range(64)]
OP_IDXS_R = [i for i in range(64)]
OOUT_IDXS = [i for i in range(64)]
OOUT_IDXS_R = [i for i in range(64)]
RIN = [i for i in range(64)]
RIN_R = [i for i in range(64)]
ROUT = [i for i in range(64)]
ROUT_R = [i for i in range(64)]

S = [i for i in range(256)]
RCI = 0
RCJ = 0

def get_swap():
    global RCI, RCJ
    RCI = (RCI + 1) % 256
    RCJ = (RCJ + S[RCI]) % 256
    S[RCI], S[RCJ] = S[RCJ], S[RCI]
    return RCI % 64, RCJ % 64

def scramble_o():
    for _ in range(312):
        i, j = get_swap()
        OP_IDXS[OP_IDXS_R[i]] = j
        OP_IDXS[OP_IDXS_R[j]] = i
        OP_IDXS_R[i], OP_IDXS_R[j] = OP_IDXS_R[j], OP_IDXS_R[i]

def scramble_oout():
    for _ in range(456):
        i, j = get_swap()
        OOUT_IDXS[OOUT_IDXS_R[i]] = j
        OOUT_IDXS[OOUT_IDXS_R[j]] = i
        OOUT_IDXS_R[i], OOUT_IDXS_R[j] = OOUT_IDXS_R[j], OOUT_IDXS_R[i]

def scramble_rin():
    for _ in range(331):
        i, j = get_swap()
        RIN[RIN_R[i]] = j
        RIN[RIN_R[j]] = i
        RIN_R[i], RIN_R[j] = RIN_R[j], RIN_R[i]

def scramble_rout():
    for _ in range(599):
        i, j = get_swap()
        ROUT[ROUT_R[i]] = j
        ROUT[ROUT_R[j]] = i
        ROUT_R[i], ROUT_R[j] = ROUT_R[j], ROUT_R[i]

ADDS = [45124, 27787, 5443, 57762, 26426, 35976, 795, 56870, 6573, 53292, 35658, 9236, 29135, 15515, 10430, 16765, 1976, 47730, 27666, 52187, 46620, 59509, 25031]

def get_noise():
    seq = [i for i in range(len(ADDS))]
    i = random.choice(seq)
    return 9 + i, ADDS[i]

OPI_INPUT = 0
OPI_OUTPUT = 1
OPI_XOR = 4
OPI_JMP = 7
OPI_ADD = 8
OPI_ADD_R = 57
OPI_OR = 6
OPI_AND = 5
OPI_NOISE = 12
OPI_UNLOCK = 56

START_SCRAMBLE = False

def make_op(c0, c1, c2, c3, opi, r1, r2, imm):
    global START_SCRAMBLE

    if START_SCRAMBLE:
        c0 = random.randint(0, 1)
        c1 = random.randint(0, 1)
        c2 = random.randint(0, 1)
        c3 = random.randint(0, 1)

    op = [0] * 32

    op[0] = str(c0)
    op[1] = str(c1)
    op[2] = str(c2)
    op[3] = str(c3)

    op[4:10] = list(bin(opi)[2:].rjust(6, '0'))[::-1]
    op[10:16] = list(bin(r1)[2:].rjust(6, '0'))[::-1]
    op[16:22] = list(bin(r2)[2:].rjust(6, '0'))[::-1]
    op[22:32] = list(bin(imm)[2:].rjust(10, '0'))[::-1]

    if len(op) > 32:
        print("???", hex(imm))

    bop = int(''.join(op)[::-1], 2)

    if c0 == 1:
        scramble_o()
    if c1 == 1:
        scramble_oout()
    if c2 == 1:
        scramble_rin()
    if c3 == 1:
        scramble_rout()

    return bop

OPS = []
# OPS.append(make_op(1, 1, 1, 1, OPI_UNLOCK, 0, 0, 0))
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[1], RIN[0], 16))

# make message
msg = "Enter flag (exactly 24 chars): "
for i in range(len(msg)):
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[8+i], RIN[0], ord(msg[i])))

# print message
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[1], RIN[0], 8))
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_OUTPUT]], ROUT[1], RIN[1], 0x0200+31))

# read input
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[1], RIN[0], 32))
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_INPUT]], ROUT[1], RIN[1], 0x0100+24))

# echo input
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[1], RIN[0], 32))
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_OUTPUT]], ROUT[1], RIN[1], 0x0200+24))

# scramble input
seq = [i for i in range(24)]
seq2 = [i for i in range(24)]
scrambled = [-1] * 24
random.shuffle(seq)
random.shuffle(seq2)
for i1, i2 in zip(seq, seq2):
    if i1 == 9:
        # unlock the nasties
        START_SCRAMBLE = True
        OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_UNLOCK]], ROUT[1], RIN[0], 0xcc))

    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[8+i1], RIN[32+i2], 0))
    scrambled[i2] = i1

# check scrambled
# OPS.append(make_op(0, 0, 0, 0, OP_IDXS[OPI_ADD], ROUT[1], RIN[0], 8))
# OPS.append(make_op(0, 0, 0, 0, OP_IDXS[OPI_OUTPUT], ROUT[1], RIN[1], 0x0200+24))

# accumulate verdict in R2
# ensure first char is g

LEFT = len(flag) - 1

OPS.append(make_op(1, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[3], RIN[8 + scrambled[0]], 0))
OPS.append(make_op(0, 1, 0, 0, OOUT_IDXS[OP_IDXS[OPI_XOR]], ROUT[2], RIN[3], ord('g')))
OPS.append(make_op(0, 0, 1, 0, OOUT_IDXS[OP_IDXS[OPI_JMP]], ROUT[1], RIN[2], 0x300 + 3))

# if first char is not g
OPS.append(make_op(0, 0, 0, 1, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[2], RIN[0], 1))
OPS.append(make_op(0, 0, 1, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[3], RIN[0], 0))
OPS.append(make_op(0, 1, 0, 0, OOUT_IDXS[OP_IDXS[OPI_JMP]], ROUT[1], RIN[3], 0x300 + 1))

OPS.append(make_op(0, 0, 0, 1, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[2], RIN[0], 0))

## make pairs
idxs = [i for i in range(1, len(flag))]
random.shuffle(idxs)

# add 2 random chars
# mix up with some random operations
curr_i = 0
for _ in range(len(idxs)):
    next_i = idxs.pop()

    rs = [3, 4, 5, 6, 7]
    random.shuffle(rs)
    r1 = rs.pop()
    r2 = rs.pop()
    r3 = rs.pop()

    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[r2], RIN[8 + scrambled[curr_i]], 0))
    for _ in range(random.randint(0, 2)):
        OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[random.randint(0, 63)]], ROUT[random.choice(rs)], RIN[random.randint(0, 63)], random.randint(0, 63)))
        LEFT -= 1
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[r3], RIN[8 + scrambled[next_i]], 0))
    for _ in range(random.randint(0, 2)):
        OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[random.randint(0, 63)]], ROUT[random.choice(rs)], RIN[random.randint(0, 63)], random.randint(0, 63)))
        LEFT -= 1

    noise1 = random.randint(0, 0xff)
    opi_noise, noise2 = get_noise()

    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD_R]], ROUT[r1], RIN[r2], RIN[r3]))
    for _ in range(random.randint(0, 2)):
        OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[random.randint(0, 63)]], ROUT[random.choice(rs)], RIN[random.randint(0, 63)], random.randint(0, 63)))
        LEFT -= 1

    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[opi_noise]], ROUT[r1], RIN[r1], noise1))
    for _ in range(random.randint(0, 2)):
        OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[random.randint(0, 63)]], ROUT[random.choice(rs)], RIN[random.randint(0, 63)], random.randint(0, 63)))
        LEFT -= 1

    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_AND]], ROUT[r1], RIN[r1], 0xff))
    for _ in range(random.randint(0, 2)):
        OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[random.randint(0, 63)]], ROUT[random.choice(rs)], RIN[random.randint(0, 63)], random.randint(0, 63)))
        LEFT -= 1

    # checking and branching if flag is correct
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_XOR]], ROUT[3], RIN[r1], ((ord(flag[curr_i]) + ord(flag[next_i]) + noise1) ^ noise2) & 0xff))
    for _ in range(random.randint(0, 2)):
        OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[random.randint(0, 63)]], ROUT[random.randint(4, 7)], RIN[random.randint(0, 63)], random.randint(0, 63)))
        LEFT -= 1
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_JMP]], ROUT[1], RIN[3], 0x300 + 3))

    # this means false
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[2], RIN[0], 1))
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[3], RIN[0], 0))
    OPS.append(make_op(0, 1, 0, 0, OOUT_IDXS[OP_IDXS[OPI_JMP]], ROUT[1], RIN[3], 0x300 + 1))

    curr_i = next_i

# sub/xor to update verdict

for _ in range(random.randint(12, 16)):
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[random.randint(0, 63)]], ROUT[random.choice([3, 4, 5, 6, 7])], RIN[random.randint(0, 63)], random.randint(0, 63)))

# control flow
fail_msg = "\nWrong password!\n"
success_msg = "\nCorrect password!\n"

# OPS.append(make_op(0, 0, 0, 0, OPI_ADD, 2, 0, 10))
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_JMP]], ROUT[1], RIN[2], 0x300 + len(fail_msg) + 4))

# default flow: print fail, then skip following
# jmp: print success

## make fail message
msg = fail_msg
for i in range(len(msg)):
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[8+i], RIN[0], ord(msg[i])))

## print fail message
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[1], RIN[0], 8))
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_OUTPUT]], ROUT[1], RIN[1], 0x0200+len(msg)))

OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[2], RIN[0], 0))
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_JMP]], ROUT[1], RIN[2], 0x300 + len(success_msg) + 2))

## make success message
msg = success_msg
for i in range(len(msg)):
    OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[8+i], RIN[0], ord(msg[i])))

## print success message
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_ADD]], ROUT[1], RIN[0], 8))
OPS.append(make_op(0, 0, 0, 0, OOUT_IDXS[OP_IDXS[OPI_OUTPUT]], ROUT[1], RIN[1], 0x0200+len(msg)))

print(OPS)