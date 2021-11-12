section .text
	global cmpstr ;make cmpstr transparent to other modules

cmpstr:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	
get_arguments:
	mov ecx, [ebp+12];ecx = char *s1
	mov edx, [ebp+16];edx = char *s2
	mov eax, 0

loop:
	cmp [ecx], BYTE 0; (*s1)='\0'
	je first_zero
	jmp compare

first_zero:
	cmp [edx], BYTE 0; (*s2)='\0'
	je FINISH; both (*s1)='\0' && (*s2)='\0'
	jmp compare

compare:
	movzx eax, BYTE [ecx]; eax = (*s1)
	movzx ebx, BYTE [edx]; ebx = (*s2)
	sub eax, ebx; eax = (*s1)- (*s2)
	cmp eax,0 
	jne FINISH; (*s1)!=(*s2) 
	inc ecx; s1++
	inc edx; s2++
	jmp loop
	
FINISH:
	mov esp, ebp ;stack maintenance
	pop ebx
	pop ebp ;stack maintenance
	ret ;stack maintenance