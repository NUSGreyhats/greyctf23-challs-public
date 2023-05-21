from pwn import *

# Change this to the challenge endpoint later
r = remote("localhost", 9999)

n = 10**128
phi = 10**127 * 9

r.sendline(str(pow(2, phi//9, n)))
r.sendline(str(10))

r.interactive()