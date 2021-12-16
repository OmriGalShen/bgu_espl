#include <sys/mman.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>

int main (int argc, char *argv[])
{
    int fd;
    char *src;

    if (argc != 2)
    {
        fprintf(stderr, "usage: ./examine <elf_file>" );
        return 1;
    }

    if( (fd = open(argv[1], O_RDONLY) ) < 0 )
    {
        fprintf(stderr, "open failed" );
        return 1;
    }

    off_t  size = lseek(fd, 0, SEEK_END);

    src = mmap (0, size, PROT_READ, MAP_SHARED, fd, 0);

    for(int i=0; i<3; i++)
    printf("[%X] ",src[i]);
    printf("\n");
    close(fd);

    return 0;
}