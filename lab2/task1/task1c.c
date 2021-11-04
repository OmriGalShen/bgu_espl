#include <stdio.h>

int main()
{
    int iarray[3];
    char carray[3];
    long dist1 = (size_t)(iarray+1) - (size_t)(iarray);
    long dist2 = (size_t)(carray+1) - (size_t)(carray);
    printf("Memory address of 'iarray':%p\n",iarray);
    printf("Memory address of 'iarray+1':%p\n",(iarray+1));
    printf("dist1: (size_t)&(iarray+1) - (size_t)(iarray): %ld\n",dist1);
    printf("Memory address of 'carray':%p\n",carray);
    printf("Memory address of 'carray+1':%p\n",(carray+1));
    printf("dist1: (size_t)&(carray+1) - (size_t)(carray): %ld\n",dist2);

    return 0;
}