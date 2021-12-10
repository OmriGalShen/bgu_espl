all: exec

exec: task1.o LineParser.o
	gcc -g -Wall -o myshell task1.o LineParser.o

task1.o: task1.c
	gcc -g -Wall -c -o task1.o task1.c

LineParser.o: LineParser.c
	gcc -g -Wall -c -o LineParser.o LineParser.c
	
.PHONY: clean val

clean:
	rm -rf *.o myshell

run: myshell
	clear
	./myshell

val: myshell
	clear
	valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         ./myshell