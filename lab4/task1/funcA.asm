section .text
	global funcA
	
funcA:
	push	ebp; save for after function finished
	push	ebx; save for after function finished
	mov	ebp, esp
	mov	eax,-1; initale value for eax with -1

.L2: ;
	add eax, 1 ;eax := i = 0,1,2,..
	mov ebx, eax; ebx = i
	add ebx, [ebp+12]; ebx = i + parameter:=a 
	movzx	ebx, BYTE [ebx]; ebx = bl + zeroes (first byte of i+a) --  exb = ebx%256
	test bl,bl ;bit-wise AND of bl (without affecting bl)
	jne .L2; loop until bl=0
	mov esp, ebp
	pop ebx; restore previous ebx
	pop ebp; restore previous ebp
	ret ; finished with eax = i s.t first byte of a + i = 0