all: exec

exec: task2.o LineParser.o
	gcc -g -Wall -o myshell task2.o LineParser.o

task2.o: task2.c
	gcc -g -Wall -c -o task2.o task2.c

LineParser.o: LineParser.c
	gcc -g -Wall -c -o LineParser.o LineParser.c
	
.PHONY: clean val

clean:
	rm -rf *.o myshell

run:
	clear
	./myshell

val: 
	clear
	valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         ./myshell