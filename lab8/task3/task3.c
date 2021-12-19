#include <stdio.h>
#include <stdlib.h>

int fib(int limit)
{
    printf("hey");
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
