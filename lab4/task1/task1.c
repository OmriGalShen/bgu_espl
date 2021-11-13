#include <stdio.h>

extern int funcA(char* str);

int main(int argc, char **argv)
{
    if(argc != 2) 
        printf("Please enter a string\n");
    else
        printf("%d\n",funcA(argv[1]));
    return 0;
}