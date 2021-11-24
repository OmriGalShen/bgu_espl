section .text
	global open; int open(const char *path, int oflag);

open:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	
sys_open:
	mov eax, 5; sys_open
	mov ebx, [ebp+12]; const char *path
	mov ecx, [ebp+16];  int oflag
	int 80h
	
FINISH:
	mov esp, ebp ;stack maintenance
	pop ebx
	pop ebp ;stack maintenance
	ret ;stack maintenance