exec: task1a.o
	gcc -g -m32 -Wall -ansi -o bcmp task1a.o

task1a.o: task1a.c
	gcc -g -m32 -Wall -ansi -c -o task1a.o task1a.c
	
task1b.o: task1b.c
	gcc -g -m32 -Wall -ansi -c -o task1b.o task1b.c

task1c.o: task1c.c
	gcc -g -m32 -Wall -ansi -c -o task1c.o task1c.c

.PHONY: clean

clean:
	rm *.o bubblesort