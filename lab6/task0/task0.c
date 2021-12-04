#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "LineParser.h"

#define MAX_READ 1<<11

int main()
{
    long size;
    char *abs_path_name;
    size = pathconf(".", _PC_PATH_MAX);
    char buf[size];
    abs_path_name = getcwd(buf, (size_t)size);

    while(1){
    printf("%s> ",abs_path_name);
    char user_input[MAX_READ];
    fgets(user_input, MAX_READ,stdin);
    if(strncmp(user_input,"quit"))
        break;
    
    cmdLine* command = parseCmdLines(user_input);
    
    
    printf("%s\n",command->arguments[0]);
    }
    
    return 0;
}