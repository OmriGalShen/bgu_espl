all:examine

examine: task0.o
	gcc -m32 -o examine task0.o

task0.o: task0.c
	gcc -c -m32 -o task0.o task0.c

.PHONY: clean

clean:
	rm -rf *.o examine