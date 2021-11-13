all: task1

task1: task1.o funcA.o
	gcc -m32 -o task1 task1.o funcA.o

task1.o: task1.c
	gcc -m32 -c -o task1.o task1.c
	
funcA.o: funcA.asm
		nasm -g -f elf -w+all -o funcA.o funcA.asm

clean:
	rm -rf *.o task0
