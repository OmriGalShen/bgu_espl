all: exec

exec: mypipe.o
	gcc -g -Wall -o mypipe mypipe.o

mypipe.o: mypipe.c
	gcc -g -Wall -c -o mypipe.o mypipe.c

.PHONY: clean val

clean:
	rm -rf *.o mypipe