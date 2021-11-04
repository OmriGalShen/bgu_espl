exec: addresses.o task1c.o
	gcc -g -m32 -Wall -ansi -o addresses addresses.o
	gcc -g -m32 -Wall -ansi -o task1c task1c.o

addresses.o: addresses.c
	gcc -g -m32 -Wall -ansi -c -o addresses.o addresses.c

task1c.o: task1c.c
	gcc -g -m32 -Wall -ansi -c -o task1c.o task1c.c

.PHONY: clean

clean:
	rm *.o addresses task1c