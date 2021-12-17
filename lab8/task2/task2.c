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
    char *section_names = (char *)(map_start + section_header[header->e_shstrndx].sh_offset);
    int index = 0;
    printf("Num:    value      section_index section_name symbol_name\n");
    for (int i = 0; i < num_of_sections; i++)
    {
        if (section_header[i].sh_type == SHT_SYMTAB)
        {
            Elf32_Sym *symtab = (Elf32_Sym *)(map_start + section_header[i].sh_offset);
            int symbol_num = section_header[i].sh_size / section_header[i].sh_entsize;
            char *symbol_names = (char *)(map_start + section_header[section_header[i].sh_link].sh_offset);
            for (int j = 0; j < symbol_num; j++)
            {
                char *symbol_name = symbol_names + symtab[j].st_name;
                char *section_name = section_names + section_header[i].sh_name;
                printf("%-2d:     %08x   %-12d  %-13s %s\n",
                       index,
                       symtab[j].st_value,
                       symtab[j].st_shndx,
                       section_name, 
                       symbol_name);
                index++;
            }
        }
    }
    
    close(fd);
    return 0;
}