all: myshell

myshell: task0.o LineParser.o 
	gcc -m32 -g -o myshell task0.o LineParser.o

LineParser.o: LineParser.c LineParser.h
	gcc -m32 -c -o LineParser.o LineParser.c

task0.o: task0.c
	gcc -m32 -c -o task0.o task0.c

.PHONY: clean

clean:
	rm -f *.o task0 LineParser
