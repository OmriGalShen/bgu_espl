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

    Elf32_Shdr *shdr = (Elf32_Shdr *)(map_start + header->e_shoff);
    int shnum = header->e_shnum;

    Elf32_Shdr *sh_strtab = &shdr[header->e_shstrndx];
    const char *const sh_strtab_p = map_start + sh_strtab->sh_offset;
    Elf32_Shdr *curr_section;
    printf("[Nr] Name                 Addr     Off      Size\n");
    for (int i = 0; i < shnum; ++i)
    {
        curr_section = (Elf32_Shdr *)(((char *)header) + header->e_shoff + i * header->e_shentsize);
        const char *section_name = sh_strtab_p + shdr[i].sh_name;
        printf("[%-2d] %-20s %08x %08x %08x\n", i,
               section_name, curr_section->sh_addr, curr_section->sh_offset, curr_section->sh_size);
    }

    close(fd);
    return 0;
}