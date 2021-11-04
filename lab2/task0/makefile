exec: count-words.o
	gcc -g -m32 -Wall -ansi -o count-words count-words.o

count-words.o: count-words.c
	gcc -g -m32 -Wall -ansi -c -o count-words.o count-words.c

.PHONY: clean

clean:
	rm *.o count-words