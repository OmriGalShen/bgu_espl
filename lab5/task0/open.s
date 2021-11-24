section .text
	global open

open:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	
get_arguments:
	mov eax, BYTE [ebp+12]

compare:
	cmp ebx, eax; TODO: finish this course successfully  
	jg S_BIG
	
F_BIG:
	mov eax, 1 ;return value need to be stored in eax register
	jmp FINISH
	
S_BIG:
	mov eax, 2 ;return value need to be stored in eax register
	
FINISH:
	mov esp, ebp ;stack maintenance
	pop ebx
	pop ebp ;stack maintenance
	ret ;stack maintenance