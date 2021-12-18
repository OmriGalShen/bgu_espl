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
	./patch task3 0000057d 122 fibonacci 0000065d
	./fibonacci 33

.PHONY: clean

clean:
	rm -rf *.o patch