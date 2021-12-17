#include <stdio.h>
#include <stdlib.h>

int fib(int limit)
{
    int a = 1, b = 1, temp;
    while (a <= limit)
    {
        printf("%d ", a);
        temp = a;
        a = b;
        b += temp;
    }
    printf("\n\nAsta la vista baby!\n\n");
}

int main(int argc, char **argv)
{
    if(argc != 2)
    {
        printf("Usage: fib <limit>");
    }
    fib(atoi(argv[1]));
}
