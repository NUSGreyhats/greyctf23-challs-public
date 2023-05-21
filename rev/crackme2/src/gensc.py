from pwn import *
from tqdm import tqdm
import string
import random

context.arch = "amd64"

random.seed(98232)

SUCCESS = 0x00000000004011f6
SUCCESS_ID = None
SUCCESS_KEY = random.randint(0, 0xffffffff)
FAILURE = 0x0000000000401217
FAILURE_ID = None
FAILURE_KEY = random.randint(0, 0xffffffff)

FLAG_RBP_OFFSET = 0x4068
FAKE_FLAG = b"apple oranges banana"
FLAG = b"grey{d1d_y0u_s0lv3_by_emul4t1ng?_1e4b8adeg}"

REGS = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"]

def pick_reg(filter=[]):
    regs = REGS.copy()
    for reg in filter:
        if reg in regs:
            regs.remove(reg)
    return random.choice(regs)

def make_number(r, n, filter=[], count=-1):
    if count == -1:
        count = random.randint(6, 10)

    val = random.randint(0, 0xffffffff)

    reg1 = pick_reg(filter + [r])
    sc = f"mov {reg1}, {val:#x}\n"
    for _ in range(count):
        tmp = random.randint(0, 0xffffffff)
        reg2 = pick_reg(filter + [r, reg1])
        op = random.randint(0, 2)

        sc += f"mov {reg2}, {tmp:#x}\n"

        if op == 0:
            sc += f"add {reg2}, {reg1}\n"
            val += tmp
        if op == 1:
            sc += f"sub {reg2}, {reg1}\n"
            val = tmp - val
        if op == 2:
            sc += f"xor {reg2}, {reg1}\n"
            val ^= tmp

        reg1 = reg2
    
    op = random.randint(0, 2)

    if op == 0:
        tmp = (n - val)
        sc += f"mov {r}, {tmp:#x}\n"
        sc += f"add {r}, {reg1}\n"
    if op == 1:
        tmp = (val + n)
        sc += f"mov {r}, {tmp:#x}\n"
        sc += f"sub {r}, {reg1}\n"
    if op == 2:
        tmp = val ^ n
        sc += f"mov {r}, {tmp:#x}\n"
        sc += f"xor {r}, {reg1}\n"

    return sc

def call_success():
    sc = f"mov rax, {SUCCESS:#x}\n"
    sc += "call rax;"
    return sc

def call_failure():
    sc = f"mov rax, {FAILURE:#x}\n"
    sc += "call rax;"
    return sc

def lea_flag():
    reg = random.choice(REGS)
    sc = make_number(reg, FLAG_RBP_OFFSET, count=4)
    sc += f"lea {reg}, [rbp + {reg}]\n"
    return reg, sc

def check_flag(i, correct):
    reg, sc = lea_flag()

    reg2 = pick_reg([reg])
    sc += make_number(reg2, i, count=random.randint(3, 5), filter=[reg])

    # this does nothing
    sc += make_number(pick_reg([reg, reg2]), random.randint(0, 0xffff), filter=[reg, reg2], count=random.randint(3, 5))

    reg3 = pick_reg([reg, reg2])
    sc += f"movzx {reg3}, BYTE PTR[{reg} + {reg2}]\n"

    reg4 = pick_reg([reg, reg2, reg3])
    sc += make_number(reg4, correct, count=random.randint(3, 5), filter=[reg, reg2, reg3])
    sc += f"sub {reg4}, {reg3}\n"
    sc += f"or r12, {reg4}\n"

    # this does nothing
    sc += make_number(pick_reg(), random.randint(0, 0xffffff), count=random.randint(3, 5))

    return sc

def bogus(i, x, y):
    reg, sc = lea_flag()

    reg2 = pick_reg([reg])
    sc += make_number(reg2, i, count=random.randint(3, 5), filter=[reg])

    # this does nothing
    sc += make_number(pick_reg([reg, reg2]), random.randint(0, 0xffff), filter=[reg, reg2], count=random.randint(3, 5))

    reg3 = pick_reg([reg, reg2])
    sc += f"movzx {reg3}, BYTE PTR[{reg} + {reg2}]\n"

    reg4 = pick_reg([reg, reg2, reg3])
    sc += make_number(reg4, x, count=random.randint(3, 5), filter=[reg, reg2, reg3])
    sc += f"xor {reg4}, {reg3}\n"

    reg5 = pick_reg([reg, reg2, reg3, reg4])
    sc += make_number(reg5, y, count=random.randint(3, 5), filter=[reg, reg2, reg3, reg4])
    sc += f"cmp {reg4}, {reg5}\n"

    # this does nothing
    sc += make_number(pick_reg(), random.randint(0, 0xffffff), count=random.randint(3, 5))

    return sc

def finale():
    global SUCCESS_ID, SUCCESS_KEY, FAILURE_ID, FAILURE_KEY
    sc = make_number("rdx", FAILURE_ID, filter=["rsi", "rax"])
    sc += make_number("rbx", SUCCESS_ID, filter=["rsi", "rax", "rdx"])
    sc += "test r12, r12\n"
    sc += "cmove rdx, rbx\n"
    sc += "mov rax, rdx\n"

    sc += make_number("rdx", FAILURE_KEY, filter=["rsi", "rax"])
    sc += make_number("rbx", SUCCESS_KEY, filter=["rsi", "rax", "rdx"])
    sc += "test r12, r12\n"
    sc += "cmove rdx, rbx\n"
    sc += "mov rcx, rdx\n"

    sc += "ret\n"

    return sc

def make_footer(nid, nk, init_r12=False):
    global SUCCESS_ID, SUCCESS_KEY, FAILURE_ID, FAILURE_KEY
    assert(SUCCESS_ID is not None)
    assert(FAILURE_ID is not None)
    # sc = shellcraft.amd64.mov('rax', 0xdeadbeef)
    # sc += shellcraft.amd64.itoa('rax')
    # sc += shellcraft.amd64.linux.write(1, 'rsp', 32)

    if init_r12:
        sc = shellcraft.amd64.linux.ptrace(0)
        sc += "mov rsi, rax\n"

        sc += make_number("rdx", nid, filter=["rsi", "rax"])
        sc += "xor r12, r12;\n"
        sc += make_number("rbx", FAILURE_ID, filter=["rsi", "rax", "rdx"])
        sc += "inc rsi\n"
        sc += "cmove rdx, rbx\n"
        sc += "mov rax, rdx\n"

        sc += make_number("rdx", nk, filter=["rsi", "rax"])
        sc += make_number("rbx", FAILURE_KEY, filter=["rsi", "rax", "rdx"])
        sc += "test rsi, rsi\n"
        sc += "cmove rdx, rbx\n"
        sc += "mov rcx, rdx\n"
    else:
        sc = make_number("rax", nid)
        sc += make_number("rcx", nk, filter=["rax"])

    sc += "ret\n"

    return sc


def compile_code(sc, key):
    sc = asm(sc)
    enc_sc = xor(sc, p32(key))
    # pad to multiple of 4
    while len(enc_sc) % 4 != 0:
        enc_sc += bytes([random.randint(0, 0xff)])

    return len(enc_sc) // 4, enc_sc

def pack_enc_sc(enc_sc):
    pck = []
    pck.append(len(enc_sc) // 4)
    for i in range(0, len(enc_sc), 4):
        pck.append(u32(enc_sc[i:i+4]))
    return pck

def main():
    global SUCCESS_ID, FAILURE_ID
    ENC_CODE = []
    TOTAL_SIZE = 8192 * 2

    SUCCESS_ID = 0
    sc = call_success()
    l, enc_sc = compile_code(sc, SUCCESS_KEY)
    ENC_CODE.extend(pack_enc_sc(enc_sc))

    FAILURE_ID = len(ENC_CODE)
    sc = call_failure()
    l, enc_sc = compile_code(sc, FAILURE_KEY)
    ENC_CODE.extend(pack_enc_sc(enc_sc))

    # do backwards
    BACK_ENC_CODE = []

    sc = finale()
    curr_key = random.randint(0, 0xffffffff)
    l, enc_sc = compile_code(sc, curr_key)
    packed = pack_enc_sc(enc_sc)
    BACK_ENC_CODE = packed + BACK_ENC_CODE
    curr_id = TOTAL_SIZE - len(packed)


    SEQ = [i for i in range(len(FLAG))]
    SEQ = SEQ + [-1] * (len(FLAG) // 2)
    SEQ = SEQ + [-2] * (len(FLAG) // 2)
    random.shuffle(SEQ)

    for i in tqdm(SEQ):
        if i == -1:
            sc = bogus(random.randint(0, len(FLAG)), random.randint(0, 0xff), random.randint(0, 0xff))
        elif i == -2:
            sc = make_number(pick_reg(), random.randint(0, 0xffffffff))
        else:
            sc = check_flag(i, FLAG[i])

        sc += make_footer(curr_id, curr_key)
        curr_key = random.randint(0, 0xffffffff)
        l, enc_sc = compile_code(sc, curr_key)
        packed = pack_enc_sc(enc_sc)
        BACK_ENC_CODE = packed + BACK_ENC_CODE
        curr_id -= len(packed)

        # print(curr_id)


    SEQ = [i for i in range(len(FAKE_FLAG))]
    random.shuffle(SEQ)
    for i in tqdm(SEQ):
        sc = bogus(i, ord(random.choice(string.ascii_letters)), SEQ[i])

        sc += make_footer(curr_id, curr_key)
        curr_key = random.randint(0, 0xffffffff)
        l, enc_sc = compile_code(sc, curr_key)
        packed = pack_enc_sc(enc_sc)
        BACK_ENC_CODE = packed + BACK_ENC_CODE
        curr_id -= len(packed)

        # print(curr_id)

    for i in tqdm(range(random.randint(4, 8))):
        sc = make_footer(curr_id, curr_key)
        curr_key = random.randint(0, 0xffffffff)
        l, enc_sc = compile_code(sc, curr_key)
        packed = pack_enc_sc(enc_sc)
        BACK_ENC_CODE = packed + BACK_ENC_CODE
        curr_id -= len(packed)

        # print(curr_id)

    sc = make_footer(curr_id, curr_key, init_r12=True)
    curr_key = random.randint(0, 0xffffffff)
    l, enc_sc = compile_code(sc, curr_key)
    packed = pack_enc_sc(enc_sc)
    BACK_ENC_CODE = packed + BACK_ENC_CODE
    curr_id -= len(packed)

    for i in tqdm(range(random.randint(10, 15))):
        sc = make_footer(curr_id, curr_key)
        curr_key = random.randint(0, 0xffffffff)
        l, enc_sc = compile_code(sc, curr_key)
        packed = pack_enc_sc(enc_sc)
        BACK_ENC_CODE = packed + BACK_ENC_CODE
        curr_id -= len(packed)

        # print(curr_id)

    STARTING_ID = curr_id
    STARTING_KEY = curr_key

    GAP_SIZE = TOTAL_SIZE - len(ENC_CODE) - len(BACK_ENC_CODE)
    GAP = [random.randint(0, 0xffffffff) for _ in range(GAP_SIZE)]
    ENC_CODE = ENC_CODE + GAP + BACK_ENC_CODE

    print(ENC_CODE)
    print("STARTING ID", STARTING_ID)
    print("STARTING KEY", STARTING_KEY)

    print("SUCCESS KEY", hex(SUCCESS_KEY))
    print("FAILURE KEY", hex(FAILURE_KEY))

    crackme_src = open("crackme.c.template", "rb").read()
    crackme_src = crackme_src.replace(b"<ENC CODE>", ",".join(map(str, ENC_CODE)).encode())
    crackme_src = crackme_src.replace(b"<STARTING ID>", str(STARTING_ID).encode())
    crackme_src = crackme_src.replace(b"<STARTING KEY>", str(STARTING_KEY).encode())

    open("crackme.c", "wb").write(crackme_src)

main()
