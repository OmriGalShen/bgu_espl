#include <stdio.h>
extern int open(const char *path, int oflag);
extern int close(int fildes);

int main(int argc, char **argv)
{
    if (argc != 2){
        fprintf(stderr,"Usage: prog filename \n");
        return 1;
    }
    int fildes=open(argv[1],0);
    printf("The corresponding file descriptor is %d \n",fildes);
    if(close(fildes) == 0){
        printf("CLOSING DONE \n");
    }
    else printf("CLOSING FAILED \n");
    return 0;
}


