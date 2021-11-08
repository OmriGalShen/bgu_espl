all: exec

exec: my_echo.c
	gcc -g -m32 -c -o my_echo.o my_echo.c
	gcc -g -m32  my_echo.o -o my_echo
	rm my_echo.o

.PHONY: clean
clean:
	rm -rf ./*.o main