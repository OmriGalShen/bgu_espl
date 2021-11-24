all: prog

prog: task0.o open.o close.o 
	gcc -m32 -o prog task0.o open.o close.o

task0.o: task0.c
	gcc -m32 -c -o task0.o task0.c
	
open.o: open.s
		nasm -g -f elf -w+all -o open.o open.s

close.o: close.s
		nasm -g -f elf -w+all -o close.o close.s

clean:
	rm -rf *.o task0
