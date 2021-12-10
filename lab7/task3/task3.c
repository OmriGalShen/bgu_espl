#include <stdlib.h>
#include "LineParser.h"
#include <limits.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <fcntl.h>

// ------- defines  --------
#define HISTORY_SIZE 5     // lab6
#define MAX_READ 2048      // lab6
#define TRUE 1             // lab6
#define FALSE 0            // lab6
#define ADD_HISTORY 1      // lab6
#define DONT_ADD_HISTORY 0 // lab6
// -----------------------

// ---  global variables ----
cmdLine *secCmd;             //lab7
cmdLine *mainCmd;            //lab6
pid_t pid;                   // lab6
char *h_array[HISTORY_SIZE]; // lab6 - History list of commands
int h_count = 0;             // lab6 - Number of total commands
int h_pointer = 0;           // lab6 - Current command index in history list
// -----------------------

// functions declarions
void general_command(cmdLine *pCmdLine);                      //lab7
void redirect_io(cmdLine *pCmdLine);                          //lab7
void general_command_pipe(cmdLine *mainCmd, cmdLine *secCmd); //lab7
int execute(cmdLine *mainCmd, cmdLine *secCmd, char pipe_f);  //lab7
void free_history();                                          //lab6
void add_history(char *cmd_str);                              //lab6
int restore_history(cmdLine *pCmdLine);                       //lab6
void print_history();                                         //lab6
// -----------------------

int main(int argc, char **argv) //lab7
{
    char cwd[PATH_MAX];
    char pipe_f = 0; // lab7 - pipe flag
    while (TRUE)
    {
        // print current working directory
        getcwd(cwd, PATH_MAX);
        printf("MyShell~%s$ ", cwd);
        // read command from user
        char input[MAX_READ];
        fgets(input, MAX_READ, stdin);
        input[strcspn(input, "\n")] = 0; // Removing trailing newline
        // quit or execute
        if (strcmp(input, "quit") == 0)
        {
            printf("exiting...\n");
            free_history();
            break;
        }
        if (strlen(input) == 0) // redundant input
            continue;

        char *first_input = strtok(input, "|"); //lab7
        char *sec_input = strtok(NULL, "|");    //lab7
        pipe_f = (sec_input) ? 1 : 0;           //lab7

        mainCmd = parseCmdLines(first_input);
        if (pipe_f)
            secCmd = parseCmdLines(sec_input);                      //lab7
        int need_history_change = execute(mainCmd, secCmd, pipe_f); //lab7
        if (need_history_change)                                    // not special case !X -> add to history
            add_history(input);
        freeCmdLines(mainCmd);
        if (pipe_f)
            freeCmdLines(secCmd);
    }
    return 0;
}

int execute(cmdLine *mainCmd, cmdLine *secCmd, char pipe_f) //lab7
{
    // check if first char of first argument is '!'
    if (mainCmd->arguments[0][0] == 33)
    {
        return restore_history(mainCmd);
    }

    // cd function
    if (strcmp(mainCmd->arguments[0], "cd") == 0)
    {
        char err = 1;
        if (mainCmd->argCount == 1)
        {
            err = chdir(getenv("HOME"));
        }
        else if (mainCmd->argCount == 2)
        {
            err = chdir(mainCmd->arguments[1]);
        }
        if (err)
            fprintf(stderr, "ERROR: Unknown direcrtory\n");
        return ADD_HISTORY;
    }

    // history function
    if (strcmp(mainCmd->arguments[0], "history") == 0)
    {
        print_history();
        return ADD_HISTORY;
    }
    if (pipe_f) //lab7
        general_command_pipe(mainCmd, secCmd);
    else
        general_command(mainCmd);
    return ADD_HISTORY;
}

void general_command_pipe(cmdLine *mainCmd, cmdLine *secCmd) //lab7
{
    int file_dec[2];
    pid_t child1_pid, child2_pid;

    if (pipe(file_dec) == -1) // STEP 1 - create a pipe
    {
        perror("pipe");
        exit(EXIT_FAILURE);
    }
    if ((child1_pid = fork()) == -1) // STEP 2 - Fork to a child process (child1).
    {
        perror("fork");
        exit(EXIT_FAILURE);
    }
    if (child1_pid == 0) // STEP 3 - child 1 - output ls -l to pipe
    {
        close(1);                                          // Close the standard output.
        dup(file_dec[1]);                                  // Duplicate the write-end of the pipe
        close(file_dec[1]);                                // Close the file descriptor that was duplicated
        execvp(mainCmd->arguments[0], mainCmd->arguments); // Execute "ls -l".
        _exit(0);                                          // returns if failed
    }
    else // parent
    {
        close(file_dec[1]); // STEP 4 - Parent Close the write end of the pipe

        if ((child2_pid = fork()) == -1) // STEP 5 - Fork again to a child process (child2).
        {
            perror("fork");
            exit(EXIT_FAILURE);
        }
        if (child2_pid == 0) // STEP 6 - child 2 - get input for pipe and perform tail
        {
            close(0);                                        // Child close the standard input.
            dup(file_dec[0]);                                // Duplicate the read-end of the pipe
            close(file_dec[0]);                              // Close the file descriptor that was duplicated
            execvp(secCmd->arguments[0], secCmd->arguments); // Execute "tail -n 2".
            _exit(0);
        }
        else //parent
        {
            close(file_dec[0]);           // STEP 7 - Parent close the read end of the pipe.
            waitpid(child1_pid, NULL, 0); // STEP 8 - wait for child1
            waitpid(child2_pid, NULL, 0); // STEP 8 - wait for child2
        }
    }
}

void general_command(cmdLine *pCmdLine) //lab7 - task1
{
    // general function - non shell
    if ((pid = fork()) == -1)
        fprintf(stderr, "ERROR: fork error\n");

    else if (pid == 0)
    {                          // code executed by child
        redirect_io(pCmdLine); // //lab7 - task1
        // execute
        execvp(pCmdLine->arguments[0], pCmdLine->arguments);

        // if execvp return, it failed
        printf("ERROR: %s command not found\n", pCmdLine->arguments[0]);

        // free all memory and exit
        free_history();
        if (pCmdLine)
            freeCmdLines(pCmdLine);
        if (mainCmd != pCmdLine)
            freeCmdLines(mainCmd);
        _exit(0);
    }
    else if (pCmdLine->blocking)
    { // code executed by parent
        waitpid(pid, NULL, 0);
    }
}

void redirect_io(cmdLine *pCmdLine) //lab7 - task1
{
    int fd;
    if (pCmdLine->inputRedirect)
    {
        fd = open(pCmdLine->inputRedirect, O_RDONLY, S_IRUSR);
        dup2(fd, 0); //replace stdin with redirect
    }
    if (pCmdLine->outputRedirect)
    {
        fd = open(pCmdLine->outputRedirect, O_WRONLY | O_CREAT | O_TRUNC, S_IWUSR);
        dup2(fd, 1); //replace stdout with redirect
    }
}

void free_history() // lab6
{
    for (int i = 0; i < HISTORY_SIZE; i++)
        free(h_array[i]);
}

void add_history(char *cmd_str) // lab6
{
    free(h_array[h_pointer]);
    h_array[h_pointer] = (char *)malloc(MAX_READ);
    strcpy(h_array[h_pointer], cmd_str);

    h_pointer++;
    h_pointer %= HISTORY_SIZE;
    h_count++;
}

void print_history() // lab6
{
    // Current command pointer inside h_array
    int h_curr_pointer = (h_count < HISTORY_SIZE) ? 0 : ((h_pointer + 1) % HISTORY_SIZE);
    // Current command index in shell
    int h_command_index = (h_count < HISTORY_SIZE) ? 0 : (h_count - HISTORY_SIZE + 1);

    /*
    Continue untill curr h_position.
    [over all, HISTORY_SIZE-1 commands will be printed: all commands
    in h_array besides the oldest command that the calling history
    command will replace in the h_array.
    (It won't be relevent to call for in the next command)]
    */
    while (h_command_index != h_count)
    {

        if (h_array[h_curr_pointer])
        {
            printf("%d) %s\n", h_command_index, h_array[h_curr_pointer]);
        }

        h_curr_pointer++;
        h_curr_pointer %= HISTORY_SIZE;
        h_command_index++;
    }
}

int restore_history(cmdLine *pCmdLine) // lab6
{
    int restored_command_index = atoi(pCmdLine->arguments[0] + sizeof(char));

    if (restored_command_index == 0 && strcmp(pCmdLine->arguments[0], "!0") != 0)
    {
        fprintf(stderr, "ERROR: didn't recognized valid number as input. try again.\n");
        return ADD_HISTORY;
    }

    if (restored_command_index >= h_count || restored_command_index < h_count - HISTORY_SIZE)
    {
        fprintf(stderr, "ERROR: history command number '%d' not found. Use 'history' command for valid options.\n", restored_command_index);
        return ADD_HISTORY;
    }

    int real_array_index = restored_command_index % HISTORY_SIZE;
    char *cmd_str = h_array[real_array_index];

    cmdLine *cmd = parseCmdLines(cmd_str);
    execute(cmd, NULL, FALSE);
    freeCmdLines(cmd);

    /*  For edge case when '!X' command will enter the same
            entry in h_array as the called command, omit adding. */
    if (real_array_index != h_pointer)
    {
        /*  Add the true function that was intended and not
                the '!X' command.
                That way, if you call a restored function that
                not in the array anymore, it won't fail. */
        add_history(cmd_str);
    }
    else
    {
        h_pointer++;
        h_pointer %= HISTORY_SIZE;
        h_count++;
    }

    // don't add the '!X' command
    return DONT_ADD_HISTORY;
}
