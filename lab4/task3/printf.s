section .rodata
    prefix db 'My character is', 0
    format db '%s %c', 10, 0

section .text
    global _start
    extern printf

_start:
    sub  esp, 4 ; allocate stack space for printf result
    push 'A' ; argument 3 to printf
    push prefix ; argument 2 to printf
    push format ; argument 1 to printf
    call printf
    add esp, 12 ; return the stack pointer to it's original location

exit:
    mov ebx, 0
    mov eax, 1
    int 80h
