exec: bubblesort.o
	gcc -g -m32 -Wall -ansi -o bubblesort bubblesort.o

bubblesort.o: bubblesort.c
	gcc -g -m32 -Wall -ansi -c -o bubblesort.o bubblesort.c

.PHONY: clean

clean:
	rm *.o bubblesort