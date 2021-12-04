#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include "LineParser.h"

#define MAX_READ 1<<11

void execute(cmdLine *pCmdLine);

char *getAbsPath();

int main() {
    char *abs_path_name = getAbsPath();

    while (1) {
        printf("%s> ", abs_path_name); //prints path

        char user_input[MAX_READ];
        fgets(user_input, MAX_READ, stdin);
        user_input[strcspn(user_input, "\n")] = 0; // Removing trailing newline

        if (strcmp(user_input, "quit") == 0) // exit condition
            break;

        cmdLine *command = parseCmdLines(user_input);
        execute(command);
        freeCmdLines(command);
    }
    return 0;
}

char *getAbsPath() {
    long max_path_len;
    max_path_len = pathconf(".", _PC_PATH_MAX);
    char buff[max_path_len];
    return getcwd(buff, (size_t) max_path_len);
}

void execute(cmdLine *pCmdLine) {
//    int res = execv(pCmdLine->arguments[0],pCmdLine->arguments); //example "/bin/ls -l"
    int res = execvp(pCmdLine->arguments[0], pCmdLine->arguments); //look for commands in your PATH setting
    if (res == -1)
        perror("execvp failed");
}