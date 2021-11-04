exec: task2a.o task2b.o task2c.o
	gcc -g -m32 -Wall -ansi -o task2a task2a.o
	gcc -g -m32 -Wall -ansi -o task2b task2b.o
	gcc -g -m32 -Wall -ansi -o task2c task2c.o

task2c.o: task2c.c 
	gcc -g -m32 -Wall -ansi -c -o task2c.o task2c.c

task2a.o: task2a.c 
	gcc -g -m32 -Wall -ansi -c -o task2a.o task2a.c

task2b.o: task2b.c
	gcc -g -m32 -Wall -ansi -c -o task2b.o task2b.c

.PHONY: clean

clean:
	rm *.o task2a task2b task2c