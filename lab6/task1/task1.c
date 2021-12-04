#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include "LineParser.h"

#define MAX_READ 1<<11
#define HISTORY_MAX_SIZE 1<<4
#define TRUE 1

char *abs_path_name;
cmdLine *historyArr[HISTORY_MAX_SIZE];
int currHistoryInd = 0;

void execute(cmdLine *pCmdLine);

void updatePath();

void add_history(cmdLine *pCmdLine);

void freeHistory();

int main() {
    while (TRUE) {
        updatePath(); // update to current absolute path
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

void updatePath() {
    long max_path_len = pathconf(".", _PC_PATH_MAX);
    char buff[max_path_len];
    abs_path_name = getcwd(buff, (size_t) max_path_len);
}

void execute(cmdLine *pCmdLine) {
    pid_t pid;
    int status;
    if (pCmdLine->argCount == 0) //empty command
        return;

    // Task1c - CD
    if (strcmp(pCmdLine->arguments[0], "cd") == 0 && pCmdLine->argCount == 2) {
        if (chdir(pCmdLine->arguments[1]) == -1) {
            fprintf(stderr, "Cannot find path %s", pCmdLine->arguments[1]);
        }
        return;
    }

    // Task1d - Print commands history
    if (pCmdLine->argCount == 1 && strcmp(pCmdLine->arguments[0], "history") == 0) {
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
    if (pCmdLine->argCount == 2 && strcmp(pCmdLine->arguments[0], "clear") == 0 &&
        strcmp(pCmdLine->arguments[1], "history") == 0) {
        freeHistory();
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