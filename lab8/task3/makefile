all:patch task3

patch: patch.o
	gcc -m32 -fno-pie -o patch patch.o

patch.o: patch.c
	gcc -c -m32 -fno-pie -o patch.o patch.c 

task3: task3.o
	gcc -m32 -fno-pie -o task3 task3.o

task3.o: task3.c
	gcc -c -m32 -fno-pie -o task3.o task3.c

run: patch task3
	clear
	./patch task3 000005bd 86 fibonacci 0000065d

.PHONY: clean

clean:
	rm -rf *.o patch