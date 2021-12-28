import os
import subprocess

MOUNT_CMD = 'mount private host:port:/server'
DEFAULT_IP = '192.168.56.1'

if __name__ == '__main__':
    is_mounting = False
    while True:
        print(f"{os.getcwd()}$ ", end='')
        user_input = input()
        if user_input == 'quit':  # exit condition
            break
        input_lst = user_input.split(' ')
        if len(input_lst) == 3 and input_lst[0] == 'mount' and input_lst[1] == 'private':
            if len(input_lst[2]) == 3:
                host, port, srv_path = input_lst[2].split(':')
                is_mounting = True
            continue
        if is_mounting and len(input_lst) == 2 and input_lst[0] == 'cd':
            host, port, srv_path = input_lst[2].split(':')

        result = subprocess.run(input_lst, capture_output=True, text=True, shell=True).stdout
        print(result)
