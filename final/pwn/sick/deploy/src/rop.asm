section .text
global _start

echo:
    push rbp
    mov rbp, rsp 
    sub rsp, 0x20
    mov r10, rsp
    push 0x200
    push r10
    call read
    push rax
    push r10
    call write
    leave
    ret

read:
    mov eax, 0
    mov edi, 0
    mov rsi, [rsp+0x8]
    mov rdx, [rsp+0x10]
    syscall
    ret

write:
    mov eax, 1
    mov edi, 1
    mov rsi, [rsp+0x8]
    mov rdx, [rsp+0x10]
    syscall
    ret

_start:
    call echo
    jmp _start