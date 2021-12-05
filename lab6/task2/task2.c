#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <limits.h>
#include "LineParser.h"

#define MAX_READ 1<<11
#define HISTORY_MAX_SIZE 1<<4
#define TRUE 1

char *abs_path_name;
cmdLine *historyArr[HISTORY_MAX_SIZE];
int currHistoryInd = 0;

void execute(cmdLine *pCmdLine);

void add_history(cmdLine *pCmdLine);

void freeHistory();

cmdLine* cmdLineCopy(cmdLine *pCmdLine);

int main() {
    char path_buff[PATH_MAX];
    while (TRUE) {
        abs_path_name = getcwd(path_buff, sizeof(path_buff)); // update to current absolute path
        printf("%s> ", abs_path_name); //prints path

        // Read user input
        char user_input[MAX_READ];
        fgets(user_input, MAX_READ, stdin);
        user_input[strcspn(user_input, "\n")] = 0; // Removing trailing newline

        if (strcmp(user_input, "quit") == 0) // exit condition
            break;

        cmdLine *command = parseCmdLines(user_input);
        execute(command);
        add_history(command);
    }
    freeHistory();
    return 0;
}

void execute(cmdLine *pCmdLine) {
    pid_t pid;
    int status;
    int argCount = pCmdLine->argCount;
    char *command = pCmdLine->arguments[0];

    if (argCount == 0) //empty command
        return;

    // Task1c - CD
    if (argCount == 2 && strcmp(command, "cd") == 0) {
        if (chdir(pCmdLine->arguments[1]) == -1) {
            fprintf(stderr, "Cannot find path %s", pCmdLine->arguments[1]);
        }
        return;
    }

    // Task1d - Print commands history
    if (argCount == 1 && strcmp(command, "history") == 0) {
        if (currHistoryInd == 0) {
            printf("No history found\n");
            return;
        }
        for (int i = 0; i < currHistoryInd; i++) {
            printf("%d  ", i);
            for (int j = 0; j < historyArr[i]->argCount; j++) {
                printf("%s ", historyArr[i]->arguments[j]);
            }
            printf("\n");
        }
        return;
    }

    // Task1d extra - clear history
    if (argCount == 2 && strcmp(command, "clear") == 0 &&
        strcmp(pCmdLine->arguments[1], "history") == 0) {
        freeHistory();
        return;
    }

    // Task2 - Reuse command
    if (argCount == 1 && command[0] == '!') {
        int ind = -1;
        sscanf(command, "!%d", &ind);
        if (ind < 0 || ind >= currHistoryInd)
            fprintf(stderr,"Invalid previous command index\n");
        else {
            cmdLine* copy = cmdLineCopy(historyArr[ind]);
            add_history(copy);
            execute(historyArr[ind]);
        }
        return;
    }

    if ((pid = fork()) == -1)
        perror("fork error");
    else if (pid == 0) { /* Code executed by child */
        execvp(pCmdLine->arguments[0], pCmdLine->arguments); //look for commands in your PATH setting
        /* If execvp returns, it must have failed. */
        printf("Unknown command\n");
        _exit(0);
    } else { /* Code executed by parent */
        if (pCmdLine->blocking)
            waitpid(pid, &status, 0);
    }
}

void freeHistory() {
    for (int i = 0; i < currHistoryInd; i++)
        freeCmdLines(historyArr[i]);
    currHistoryInd = 0;
}

void add_history(cmdLine *pCmdLine) {
    if (currHistoryInd >= HISTORY_MAX_SIZE) {
        freeHistory();
    }
    historyArr[currHistoryInd] = pCmdLine;
    currHistoryInd++;
}

cmdLine* cmdLineCopy(cmdLine *pCmdLine){
    char str[MAX_READ];
    str[0]='\0';
    for(int i=0;i<pCmdLine->argCount;i++)
    {
        strcat(str,pCmdLine->arguments[i]);
    }
    return parseCmdLines(str);
}