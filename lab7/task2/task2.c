#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>

int main()
{
    int file_dec[2];
    pid_t child1_pid, child2_pid;
    char *cmd_ls[] = {"ls", "-l", NULL};
    char *cmd_tail[] = {"tail", "-n", "2", NULL};

    if (pipe(file_dec) == -1)
    {
        perror("pipe");
        exit(EXIT_FAILURE);
    }
    if ((child1_pid = fork()) == -1)
    {
        perror("fork");
        exit(EXIT_FAILURE);
    }
    if (child1_pid == 0) // child 1 - output ls -l to pipe
    {
        close(1);                  // Close the standard output.
        dup(file_dec[1]);          // Duplicate the write-end of the pipe
        close(file_dec[1]);        // Close the file descriptor that was duplicated
        execvp(cmd_ls[0], cmd_ls); // Execute "ls -l".
        _exit(0);                  // returns if failed
    }
    else // parent
    {
        close(file_dec[1]); //Parent Close the write end of the pipe.

        if ((child2_pid = fork()) == -1)
        {
            perror("fork");
            exit(EXIT_FAILURE);
        }
        if (child2_pid == 0) // child 2 - get input for pipe and perform tail
        {
            close(0);                      // Child close the standard input.
            dup(file_dec[0]);              // Duplicate the read-end of the pipe
            close(file_dec[0]);            // Close the file descriptor that was duplicated
            execvp(cmd_tail[0], cmd_tail); // Execute "tail -n 2".
            _exit(0);
        }
        else //parent
        {
            close(file_dec[0]);           // Parent close the read end of the pipe.
            waitpid(child1_pid, NULL, 0); // wait for child1
            waitpid(child2_pid, NULL, 0); // wait for child2
        }
    }

    return (0);
}
