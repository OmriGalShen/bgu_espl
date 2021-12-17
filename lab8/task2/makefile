all:examine

examine: task2.o
	gcc -m32 -o examine task2.o

task2.o: task2.c
	gcc -c -m32 -o task2.o task2.c

.PHONY: clean

clean:
	rm -rf *.o task2