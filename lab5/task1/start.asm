section .text
	
global _start
global read; int read(int fd, char *buf, int size);
global write; int write(int fd, char *buf, int size);
global open; int open(char *name, int flags);
global close; int close(int fd);
global strlen; int strlen(char *s);

extern main; int main(int argc, char **argv)
_start:
	mov ebx,dword [esp]
	mov ecx, esp
	add ecx, 4
	push ecx; char **argv
	push ebx; int argc 
	call	main
    mov     ebx,eax
	mov	eax,1
	int 0x80

return_main:
	mov esp, ebp ;stack maintenance
	pop ebx
	pop ebp ;stack maintenance
	ret ;stack maintenance

; int read(int fd, char *buf, int size);
read:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	mov eax,3; sys_read
	mov ebx, [ebp+12]; int fd
	mov ecx, [ebp+16]; char *buf
	mov edx, [ebp+20]; int sizeSS
	int 80h
	jmp return_main

; int write(int fd, char *buf, int size);
write:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	mov eax,4; sys_write
	mov ebx, [ebp+12]; int fd
	mov ecx, [ebp+16]; char *buf
	mov edx, [ebp+20]; int size
	int 80h
	jmp return_main

; int open(char *name, int flags);
open:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	mov eax,5; sys_open
	mov ebx, [ebp+12]; char *name
	mov ecx, [ebp+16]; int flags
	int 80h
	jmp return_main

; int close(int fd);
close:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	
	mov eax,6; sys_close
	mov ebx, [ebp+12]; int fd
	int 80h
	jmp return_main

; int strlen(char *s);	
strlen:
	push ebp ;stack maintenance
	push ebx
	mov ebp, esp ;stack maintenance
	mov eax, 0
	mov ebx, [ebp+12]; char *s
strlen_loop:
	cmp [ebx], BYTE 0
	je return_main
	inc eax
	inc ebx
	jmp strlen_loop
