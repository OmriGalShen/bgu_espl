#include <stdio.h>
extern int open(const char *filename, int mode);
extern int close(int des);

int main(int argc, char **argv)
{
    if (argc != 2){
        fprintf(stderr,"Usage: prog filename \n");
        return 1;
    }
    int des=open(argv[1],0);
    printf("The corresponding file descriptor is %d \n",des);
    if(close(des)==0){
        printf("CLOSING DONE \n");
    }
    else printf("CLOSING FAILED \n");
    return 0;
}


