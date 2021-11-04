exec: bubblesort.o task0b.o
	gcc -g -m32 -Wall -ansi -o bubblesort bubblesort.o
	gcc -g -m32 -Wall -ansi -o hexaPrint task0b.o

bubblesort.o: bubblesort.c
	gcc -g -m32 -Wall -ansi -c -o bubblesort.o bubblesort.c
	
task0b.o: task0b.c
	gcc -g -m32 -Wall -ansi -c -o task0b.o task0b.c

.PHONY: clean

clean:
	rm *.o bubblesort