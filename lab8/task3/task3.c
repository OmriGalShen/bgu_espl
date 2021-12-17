#include <stdio.h>

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
    printf("\n");
}

int main(int argc, char **argv)
{
    fib(33);
}
