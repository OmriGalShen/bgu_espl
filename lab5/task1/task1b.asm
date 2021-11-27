%define UTOA_BUFLEN 16

section .bss
str: RESB UTOA_BUFLEN

section .text
	global utoa_s
    global atou_s 

;char *utoa_s(int i)
utoa_s:
	;stack maintenance
    push ebp 
	push ebx
	mov ebp, esp
    
	mov ebx, dword [ebp+12] ;ebx = i
	mov ecx, str+UTOA_BUFLEN-1; last char
    mov [ecx], BYTE 0; str[UTOA_BUFLEN-1] = 0;
	cmp ebx, 0; i==0
	je isZero; edge case

whileNotZero:	
	cmp ebx, 0; i==0
	jne nextDigit
	mov eax, ecx
	jmp FINISH
	
nextDigit:	
	dec ecx
	mov eax, ebx; eax = i
	mov edx, 0; clear edx
	mov ebx, 10
	div ebx; eax = i/10, dl = i%10
	add edx, '0'
	mov [ecx], dl
	mov ebx, eax; ebx = i/10
	jmp whileNotZero

isZero:; edge case
	dec ecx
	mov [ecx], BYTE '0'
	mov eax, ecx
	jmp FINISH

test: 
	mov eax, ecx
	jmp FINISH

;int atou_s(char* c)
atou_s:
    push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
    mov eax, dword [ebp+12] ;char* c
    jmp FINISH

FINISH:
	mov esp, ebp
	pop ebx
	pop ebp 
	ret