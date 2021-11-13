%define X 'A'
%define STR string1

section .rodata
    print_format db '"%c" appears in "%s" %d times', 10, 0
    string1 db 'ABBA', 0
    string2 db 'BBA', 0
    string3 db 'BB', 0
    string4 db '', 0
    string5 db 'SSAASSS', 0

section .text
    global _start
    extern printf

_start:
    sub  esp, 4 ; allocate stack space for printf result
    mov eax, 0; char counter
    mov ebx, STR; current char

count_loop:
    cmp [ebx], BYTE 0; end of string
    je print_res; print result
    cmp [ebx], BYTE X; current char is x
    je found_char
    inc ebx; next char
    jmp count_loop

found_char:
    inc eax; eax++
    inc ebx; next char
    jmp count_loop

print_res:
    push eax ; argument 4 to printf
    push STR ; argument 3 to printf
    push X ; argument 2 to printf
    push print_format ; argument 1 to printf
    call printf
    add esp, 16 ; return the stack pointer to it's original location
    
exit:
    mov ebx, 0
    mov eax, 1
    int 80h