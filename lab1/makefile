all: exec

task1a: task1a.c
	gcc -g -m32 -c -o task1a.o task1a.c

task1b: task1b.c
	gcc -g -m32 -c -o task1b.o task1b.c

task1c: task1c.c
	gcc -g -m32 -c -o task1c.o task1c.c

task2: task2.c
	gcc -g -m32 -c -o task2.o task2.c

exec: task1a task1b task1c task2
	gcc -g -m32  task1a.o task1b.o task1c.o task2.o -o char2ascii
	rm task1a.o task1b.o task1c.o task2.o

.PHONY: clean
clean:
	rm -rf ./*.o main
