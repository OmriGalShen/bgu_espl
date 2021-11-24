section .text
	global close ;make my_cmp transparent to other modules

close:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	
get_arguments:
	movzx eax, BYTE [ebp+12] ;retrieves the first function argument, READ about MOVZX
	movzx ebx, BYTE [ebp+16] ;retrieves the second function argument, READ about MOVZX

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