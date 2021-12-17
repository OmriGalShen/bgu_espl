#include <sys/mman.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include <elf.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    int src_fd, des_fd;

    if (argc != 6)
    {
        fprintf(stderr, "usage: ./patch source_file source_pos size dest_file dest_pos");
        return 1;
    }
    // -----------Parse command line input-----------
    if ((src_fd = open(argv[1], O_RDONLY)) < 0)
    {
        fprintf(stderr, "source_file open failed");
        return 1;
    }
    size_t src_file_size = lseek(src_fd, 0, SEEK_END);
    // size_t src_pos = atoi(argv[2]);
    int src_pos = (int)strtol(argv[2], NULL, 16);
    size_t copy_size = atoi(argv[3]);
    if ((des_fd = open(argv[4], O_RDWR | O_CREAT, 0666)) < 0)
    {
        fprintf(stderr, "dest_file open failed");
        return 1;
    }
    size_t des_file_size = lseek(des_fd, 0, SEEK_END);
    // size_t dest_pos = atoi(argv[5]);
    int dest_pos = (int)strtol(argv[5], NULL, 16);
    // ----------------------------------------------
    char *src_map = mmap(NULL, src_file_size, PROT_READ, MAP_PRIVATE, src_fd, 0);
    char *des_map = mmap(NULL, des_file_size, PROT_READ | PROT_WRITE, MAP_SHARED, des_fd, 0);

    printf("addr1:%x, addr2:%x\n",src_pos,dest_pos);

    memcpy(src_map + src_pos, des_map + dest_pos, copy_size);

    munmap(src_map, src_file_size);
    munmap(des_map, des_file_size);

    close(src_fd);
    close(des_fd);

    return 0;
}