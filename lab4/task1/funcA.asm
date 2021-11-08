section .text
	global funcA
	
funcA:
	push	ebp
	push	ebx
	mov	ebp, esp
	mov	eax,-1

.L2:
	add eax, 1
	mov ebx, eax
	add ebx, [ebp+12]
	movzx	ebx, BYTE [ebx]
	test bl,bl
	jne .L2
	mov esp, ebp
	pop ebx
	pop ebp
	ret