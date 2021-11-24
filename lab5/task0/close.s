section .text
	global close; int close(int fildes);

close:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	
sys_close:
	mov eax, 6; sys_close
	mov ebx, [ebp+12]; int fildes
	int 80h
	
FINISH:
	mov esp, ebp ;stack maintenance
	pop ebx
	pop ebp ;stack maintenance
	ret ;stack maintenance