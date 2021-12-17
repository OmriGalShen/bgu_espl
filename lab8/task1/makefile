all:examine

examine: task1.o
	gcc -m32 -o examine task1.o

task1.o: task1.c
	gcc -c -m32 -o task1.o task1.c

.PHONY: clean

clean:
	rm -rf *.o examine