all: scmp1

scmp1: scmp.o
	gcc -m32 -o scmp1 scmp.o

cmpstr1.o: cmpstr.c
	gcc -m32 -c -o cmpstr1.o cmpstr.c

scmp.o: scmp.c
	gcc -m32 -c -o scmp.o scmp.c
	
.PHONY: clean

clean:
	rm -rf *.o scmp1