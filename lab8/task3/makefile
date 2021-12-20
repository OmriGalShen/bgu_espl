all:patch task3 fibonacci

patch: patch.o
	gcc -m32 -fno-pie -o patch patch.o

patch.o: patch.c
	gcc -c -m32 -fno-pie -o patch.o patch.c 

task3: task3.o
	gcc -m32 -fno-pie -o task3 task3.o

task3.o: task3.c
	gcc -c -m32 -fno-pie -o task3.o task3.c

fibonacci: fibonacci.o
	gcc -m32 -fno-pie -o fibonacci fibonacci.o

fibonacci.o: fibonacci.c 
	gcc -c -m32 -fno-pie -o fibonacci.o fibonacci.c

run: patch task3
	./patch task3 64d 73 fibonacci 64d
	./fibonacci 33

read1: 
	readelf -s task3

read2:
	readelf -s fibonacci

dis1: task3
	objdump -d -R task3

dis2: fibonacci
	objdump -d -R fibonacci

reset: 
	make clean
	make fibonacci
	clear

.PHONY: clean

clean:
	rm -rf *.o patch task3 fibonacci