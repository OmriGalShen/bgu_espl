section .text
	
global _start
global read
global write
global open
global close
global strlen

extern main
_start:

	;TODO: handles command line input parameters
	
	call	main
    mov     ebx,eax
	mov	eax,1
	int 0x80

read:
write:
open:
close:
strlen:
	ret
