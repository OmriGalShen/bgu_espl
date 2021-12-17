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
        fprintf(stderr, "Invalid elf file format\n");
        return 1;
    }

    Elf32_Shdr *section_header = (Elf32_Shdr *)(map_start + header->e_shoff);
    int num_of_sections = header->e_shnum;
    Elf32_Shdr *sh_strtab = &section_header[header->e_shstrndx];
    const char *const sh_strtab_p = map_start + (sh_strtab)->sh_offset;

    printf("[Nr] Name                 Addr     Off      Size\n");
    for (int i = 0; i < num_of_sections; ++i)
    {
        const char *section_name = sh_strtab_p + section_header[i].sh_name;
        Elf32_Addr addr = section_header[i].sh_addr;
        Elf32_Off offset = section_header[i].sh_offset;
        Elf32_Word size = section_header[i].sh_size;
        printf("[%-2d] %-20s %08x %08x %08x\n", i,
               section_name, addr, offset, size);
    }

    close(fd);
    return 0;
}