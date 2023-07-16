nasm -f elf64 rop.asm -o output.o
ld -no-pie -z noexecstack output.o -o chall 
mv ./chall ../