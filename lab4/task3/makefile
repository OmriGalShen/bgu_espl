all: task3

task3: task3.o
	ld -melf_i386 -o task3 task3.o -lc -I/lib/ld-linux.so.2 

task3.o: task3.s
	nasm -g -f elf -w+all -o task3.o task3.s
	
.PHONY: clean

clean:
	rm -rf *.o task3