calls 512 functions deep, to create enough space on the stack, and also to obfuscate

dont mind messing up the stack
manually set return address later

actual functionality: 
pass flag pointer via register r10, can hide from compiler

helpers:
- mmaper
- inswriter

hidden function that allocates rwx memory using syscall
create mmap wrapper that takes the same arguments, but is inline and calls syscall instruction using inline asm

instructions are slowly decrypted into the memory region
- check sum of pairs of chars
- reference magic numbers to confuse (md5, tea, aes)
- xor parts of the flag
- hex encode parts of the flag
- ptrace traceme check - jump to print wrong flag message

condition satisfied => correct subsequent instructions
else => bogus instructions
- sub then cmov to replace return address

plan
1. replace return address in f512
2. make mmap helper
3. make inswriter

rop sequence:
- mmap -> inswriter -> code

rbp to be constant offset from flag

plan:
1. make ptrace traceme shellcode
2. make magic numbers shellcode
3. make random xor with flag shellcode
4. make random add/sub/mul with flag shellcode
5. make completely useless shellcode
6. 