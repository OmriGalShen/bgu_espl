#include <stdio.h>
#include <stdlib.h>

void printer(int num)
{
    printf("%d ", num);
}

int fib(int limit)
{
    int a = 0, b = 1, temp = 1, last_a = -1, i;

    while (a<=limit) {
        printer(a);
        last_a = a;
        temp += a;
        a = b;
        b = temp;
    }

    return last_a;
}

void goodbye(int limit, int last) {

    for (int i = 0; i < 100; i++)
        printf("%s", "");

    char s[] = "Fvsflb";

    for (int i = 0; i < 6; i++)
        s[i]--;

    printf("\n\n%s!\n\n", last < limit ? s : "Asta la vista baby");
}

int main(int argc, char **argv)
{
    int res;

    if (argc < 2) {
        printf("Usage: fib <limit>\n");
        exit(1);
    }

    res = fib(atoi(argv[1]));
    goodbye(atoi(argv[1]), res);

    return 0;
}