#include <stdio.h>
char *utoa_s(int i); // task1b
int atou_s(char* c);// task1b

int main(int argc, char **argv)
{
    int num = 123;
    // char* str = "5678";
    char* str = "1111";
    printf("utoa_s(%d): \"%s\"\n",num,utoa_s(num));
    printf("atou_s(\"%s\"): %d\n",str,atou_s(str));
    return 0;
}

