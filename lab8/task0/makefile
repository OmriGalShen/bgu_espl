all:examine

examine: examine.o
	gcc -m32 -o examine examine.o

examine.o: examine.c
	gcc -c -m32 -o examine.o examine.c

.PHONY: clean

clean:
	rm -rf *.o examine