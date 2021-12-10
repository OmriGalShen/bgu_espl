#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>

int main(int argc, char **argv)
{
    char debug_f = ((argc == 2) && strcmp(argv[1], "-d") == 0) ? 1 : 0;
    int file_dec[2];
    pid_t child1_pid, child2_pid;
    char *cmd_ls[] = {"ls", "-l", NULL};
    char *cmd_tail[] = {"tail", "-n", "2", NULL};

    if (pipe(file_dec) == -1) // STEP 1 - create a pipe
    {
        perror("pipe");
        exit(EXIT_FAILURE);
    }
    if (debug_f)
        fprintf(stderr, "(parent_process>forking…)\n");
    if ((child1_pid = fork()) == -1) // STEP 2 - Fork to a child process (child1).
    {
        perror("fork");
        exit(EXIT_FAILURE);
    }
    if (child1_pid == 0) // STEP 3 - child 1 - output ls -l to pipe
    {
        if (debug_f)
            fprintf(stderr, "(child1>redirecting stdout to the write end of the pipe…)\n");
        close(1);           // Close the standard output.
        dup(file_dec[1]);   // Duplicate the write-end of the pipe
        close(file_dec[1]); // Close the file descriptor that was duplicated
        if (debug_f)
            fprintf(stderr, "(child2>going to execute cmd: …)\n");
        execvp(cmd_ls[0], cmd_ls); // Execute "ls -l".
        _exit(0);                  // returns if failed
    }
    else // parent
    {
        if (debug_f)
        {
            fprintf(stderr, "(parent_process>created process with id: %d)\n", child1_pid);
            fprintf(stderr, "(parent_process>closing the write end of the pipe…)\n");
        }
        close(file_dec[1]); // STEP 4 - Parent Close the write end of the pipe

        if ((child2_pid = fork()) == -1) // STEP 5 - Fork again to a child process (child2).
        {
            perror("fork");
            exit(EXIT_FAILURE);
        }
        if (child2_pid == 0) // STEP 6 - child 2 - get input for pipe and perform tail
        {
            if (debug_f)
                fprintf(stderr, "(child2>redirecting stdin to the read end of the pipe…)\n");
            close(0);           // Child close the standard input.
            dup(file_dec[0]);   // Duplicate the read-end of the pipe
            close(file_dec[0]); // Close the file descriptor that was duplicated
            if (debug_f)
                fprintf(stderr, "(child2>going to execute cmd: …)\n");
            execvp(cmd_tail[0], cmd_tail); // Execute "tail -n 2".
            _exit(0);
        }
        else //parent
        {
            if (debug_f)
                fprintf(stderr, "(parent_process>closing the read end of the pipe…)\n");
            close(file_dec[0]); // STEP 7 - Parent close the read end of the pipe.
            if (debug_f)
                fprintf(stderr, "(parent_process>waiting for child processes to terminate…)\n");
            waitpid(child1_pid, NULL, 0); // STEP 8 - wait for child1
            waitpid(child2_pid, NULL, 0); // STEP 8 - wait for child2
        }
    }
    if (debug_f)
        fprintf(stderr, "(parent_process>exiting…)\n");
    return 0;
}
