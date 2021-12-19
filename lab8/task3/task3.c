#include <stdio.h>
#include <stdlib.h>

void printer(int num)
{
    printf("%d ", num);
}

int fib(int limit)
{
    int a = 0, b = 1, temp = -1;
    while (a <= limit)
    {
        printer(a);
        temp = a;
        a = b;
        b += temp;
    }
    return temp;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Usage: fib <limit>");
    }
    fib(atoi(argv[1]));
    printf("\n");
}
