import lief

from pwn import asm, disasm, p32, p64, xor

binary = lief.parse("./crackme3")
text = binary.get_section(".text")
seg = next(text.segments)
seg.flags = lief.ELF.SEGMENT_FLAGS(7)   # rwx
binary.write("./crackme3")

crackme = open("crackme3", "rb").read()
MARK1 = crackme.index(p64(0xc74c07caf913bfd6))
MARK2 = crackme.index(p64(0xbc6ade3ba82a4501))

CALL_CODE = crackme[MARK1+8:MARK2]

sc = "mov eax, eax\nmov ebx, ebx\nmov ecx, ecx\nmov edx, edx\n" * 4
sc = asm(sc, arch="amd64") + b"\x90"
assert(len(sc) == MARK2 - MARK1 + 8)

crackme = list(crackme)
crackme[MARK1:MARK2+8] = list(sc)
crackme = bytes(crackme)

assert(len(CALL_CODE) == 17)
assert(len(sc[8:-8]) == 17)
# print(xor(CALL_CODE, crackme[MARK1+8:MARK2]))
# print(xor(CALL_CODE, sc[8:-8]))
crackme = crackme.replace(b"NASTYKEY!NASTYKEY!", xor(CALL_CODE + b"\x90", sc[8:-7]))
crackme = crackme.replace(p32(0x5733a96b), p32(236))

# print(CALL_CODE)
# print(disasm(CALL_CODE, arch="amd64"))
open("crackme3", "wb").write(crackme)