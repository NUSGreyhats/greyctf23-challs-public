operations:
- input
- output
- mul
- div
- xor
- or
- and
- jmp - only forward jump - only jump if A = 0 - merely skips the instructions n times
(8)

- 8 add - variants with diff xor on result
- 8 sub - variants with diff xor on result
- 8 left shift
- 8 right shift
- 7 bitmask
(39)

16 nops

every instruction is of the format
OP R1 R2 IMM
R1 is dest
R2 is src

f57 unlocks the nasty code

