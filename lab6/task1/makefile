all: myshell

myshell: task1.o LineParser.o 
	gcc -m32 -g -o myshell task1.o LineParser.o

LineParser.o: LineParser.c LineParser.h
	gcc -m32 -c -o LineParser.o LineParser.c

task1.o: task1.c
	gcc -m32 -c -o task1.o task1.c

val: myshell
	valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         ./myshell

run: myshell
	clear
	./myshell

.PHONY: clean

clean:
	rm -f *.o task1 LineParser
