%.o: %.asm
	nasm -g -O1 -f elf -o $@ $<

%.o: %.c
	gcc -m32 -g -nostdlib -fno-stack-protector -c -o $@ $<

all: lwca

lwca: lwc.o start.o task1b.o 
	ld  -melf_i386 -o $@ $^

task1c: task1c.c task1b.asm
	nasm -g -f elf -w+all -o task1b.o task1b.asm
	gcc -m32 -c -o task1c.o task1c.c
	gcc -m32 -o task1c task1c.o task1b.o

clean:
	rm -f *.o lwca
