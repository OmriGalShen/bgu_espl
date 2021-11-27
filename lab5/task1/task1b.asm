%define UTOA_BUFLEN 16 ; for utoa_s

section .bss
str: RESB UTOA_BUFLEN ; for utoa_s

section .data
length: dd 0; for atou_s
count: dd 0; for atou_s

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
	add edx, '0' ; convert from number to ASCII
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
    mov ebx, dword [ebp+12] ;char* c
	mov edx, 0 
	mov ecx, ebx

get_string_length:
	cmp [ecx], BYTE 0
	je string_loop
	inc dword [length]
	inc ecx
	jmp get_string_length

string_loop:
	cmp [ebx], BYTE 0
	je result
	movzx eax, BYTE [ebx]; current char*
	sub eax, '0'; convert ascii to int

init_mul_loop:
	mov ecx, dword [length]
	mov [count], ecx
	mov ecx, 10

mul_loop:; eax = eax*10*(length-1)
	cmp [count], dword 1
	je done_mul
	mul ecx; eax = 10*eax
	dec dword [count]
	jmp mul_loop

done_mul:
	add edx, eax
	dec dword [length]
	inc ebx
	jmp string_loop

result:
	mov eax, edx
	jmp FINISH

FINISH:
	mov esp, ebp
	pop ebx
	pop ebp 
	ret