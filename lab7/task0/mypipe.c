#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    int file_des[2];
    pid_t child_pid;
    char message[] = "Hello!\n";

    pipe(file_des);

    if ((child_pid = fork()) == -1)
    {
        perror("fork");
        exit(1);
    }

    if (child_pid == 0)
    {
        close(file_des[0]); //Child process does not need this end of the pipe

        /* Send "string" through the output side of pipe */
        write(file_des[1], message, (strlen(message) + 1));
        exit(0);
    }
    else
    {
        /* Parent process closes up output side of pipe */
        close(file_des[1]); //Parent process does not need this end of the pipe

        char read_buffer[1 << 7];
        /* Read in a string from the pipe */
        read(file_des[0], read_buffer, sizeof(read_buffer));
        printf("Child message: %s", read_buffer);
    }

    return (0);
}
