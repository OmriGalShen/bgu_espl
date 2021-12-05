all: myshell

myshell: task2.o LineParser.o 
	gcc -m32 -g -o myshell task2.o LineParser.o

LineParser.o: LineParser.c LineParser.h
	gcc -m32 -c -o LineParser.o LineParser.c

task2.o: task2.c
	gcc -m32 -c -o task2.o task2.c

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
	rm -f *.o task2 LineParser
