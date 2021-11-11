section .text
	global cmpstr ;make my_cmp transparent to other modules

cmpstr:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	
get_arguments:
	mov eax, [ebp+12]
	movzx eax,BYTE [eax]
	mov ebx, [ebp+16] 
	movzx ebx,BYTE [ebx] 
    

compare:
	sub eax, ebx
	
FINISH:
	mov esp, ebp ;stack maintenance
	pop ebx
	pop ebp ;stack maintenance
	ret ;stack maintenance