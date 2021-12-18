#include <stdio.h>
#include <stdlib.h>

int fib(int limit)
{
    int a = 1;
    int b = 1;
    int c = a + b;
    return 20;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Usage: fib <limit>");
    }
    fib(atoi(argv[1]));
}
