#include <sys/mman.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include <elf.h>

int main(int argc, char *argv[])
{
    int fd;
    char *src;

    if (argc != 2)
    {
        fprintf(stderr, "usage: ./examine <elf_file>");
        return 1;
    }

    if ((fd = open(argv[1], O_RDONLY)) < 0)
    {
        fprintf(stderr, "open failed");
        return 1;
    }

    off_t size = lseek(fd, 0, SEEK_END);
    void *map_start = mmap(0, size, PROT_READ, MAP_SHARED, fd, 0);
    Elf32_Ehdr *header = (Elf32_Ehdr *)map_start;

    if (size < 5 || !(header->e_ident[0] == 0x7f && header->e_ident[1] == 'E' && header->e_ident[2] == 'L' && header->e_ident[3] == 'F'))
    {
        fprintf(stderr, "open invalid elf file format");
        return 1;
    }
    // ----------------------------------------
    printf("Bytes 1,2,3 of the magic number (in ASCII): ");
    for (int i = 1; i < 4; i++)
        printf("%c ", header->e_ident[i]);
    printf("\n");
    // ----------------------------------------
    printf("The data encoding scheme of the object file: ");
    printf("%u\n", header->e_ident[5]);
    // ----------------------------------------
    printf("Entry point (hexadecimal address): ");
    printf("%p\n", (Elf32_Addr *)(header->e_entry));
    // ----------------------------------------
    printf("The file offset in which the section header table resides: ");
    printf("%p\n", (Elf32_Off *)(header->e_shoff));
    // ----------------------------------------
    printf("The number of section header entries: ");
    printf("%d\n", (header->e_shnum));
    // ----------------------------------------
    printf("The size of each section header entry: ");
    printf("%d\n", (header->e_shentsize));
    // ----------------------------------------
    printf("The index of the shstrtab in the section header: ");
    printf("%d\n", (header->e_shstrndx));
    // ----------------------------------------

    close(fd);
    return 0;
}