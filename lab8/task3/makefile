all:patch task3

patch: patch.o
	gcc -m32 -fno-pie -o patch patch.o

patch.o: patch.c
	gcc -c -m32 -fno-pie -o patch.o patch.c 

task3: task3.o
	gcc -m32 -fno-pie -o task3 task3.o

task3.o: task3.c
	gcc -c -m32 -fno-pie -o task3.o task3.c

.PHONY: clean

clean:
	rm -rf *.o patch