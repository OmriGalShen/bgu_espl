import random
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path, PurePath

from client.network_helper import *

# To run on linux:
# mount private 192.168.56.1:500:/Server
# cd 192.168.56.1:500:/Server

# To run on both windows and linux:
# mount shared 192.168.56.1:500:Server
# mount private 192.168.56.1:500:Server
# cd 192.168.56.1:500:Server

display_path = os.getcwd()  # global for use of 2 threads
shared_shell_lock = threading.Lock()
shared_shell_blocking: bool = False  # global for use of 2 threads


class ServerInfo:
    def __init__(self, host_ip, port, base_path):
        self.base_path = base_path
        self.port = int(port)
        self.host_ip = host_ip

    def __eq__(self, other):
        return self.host_ip == other.host_ip and self.port == other.port and self.base_path == other.base_path

    def get_address(self):
        return self.host_ip, self.port


def is_child_path(parent, child):
    return not Path(child).is_absolute() and PurePath(child).is_relative_to(parent)


def shared_shell_receive_loop(client_sock):
    global display_path, shared_shell_lock
    while True:
        shared_shell_lock.acquire()
        res, _ = client_sock.recvfrom(BUFFER_SIZE)
        res = res.decode('utf-8').split(' ')
        rem_path = res[0]
        rem_cmd = ' '.join(res[1:])
        display_path = rem_path
        print()
        print(f"/{rem_path}$ {rem_cmd}")
        res, _ = client_sock.recvfrom(BUFFER_SIZE)
        cmd_output = res.decode('utf-8')
        if len(cmd_output) > 0:
            print(cmd_output)
        shared_shell_lock.release()
        time.sleep(1)


if __name__ == '__main__':
    is_mounted = False
    is_shared_shell = False
    server = None
    is_client_shell = True

    client_host = socket.gethostbyname(socket.gethostname())
    client_port = random.randint(6000, 10000)
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.bind((client_host, client_port))

    while True:
        print(f"/{display_path}$ ", end='')
        cmd = input()

        cmd_lst = cmd.split(' ')
        if cmd == 'quit' or cmd == 'exit':  # exit condition
            if is_shared_shell:
                remote_logout(sock, server.get_address())
            sys.exit()

        if is_client_shell:
            if len(cmd_lst) == 3 and cmd_lst[0] == 'mount' \
                    and cmd_lst[1] == 'private':  # mount private host:port:path
                server = ServerInfo(*cmd_lst[2].split(':'))  # host_ip:port:path
                if valid_remote_path(sock, server.get_address(), server.base_path) is True:
                    is_mounted = True
                else:
                    server = None
                    is_mounted = False
                    print('Invalid remote remote shell')
                continue

            if len(cmd_lst) == 3 and cmd_lst[0] == 'mount' \
                    and cmd_lst[1] == 'shared':  # mount private host:port:path
                server = ServerInfo(*cmd_lst[2].split(':'))  # host_ip:port:path
                is_mounted = True
                is_shared_shell = True
                continue

            elif cmd_lst[0] == 'cd' and len(cmd_lst) == 2:  # cd command on client
                cd_path = cmd_lst[1]
                cd_path_lst = cd_path.split(':')
                if is_mounted and len(cd_path_lst) == 3:  # cd host:port:path
                    cd_server = ServerInfo(*cd_path_lst)
                    if cd_server == server:  # same as mount command
                        if is_shared_shell:  # remote shared shell
                            remote_login(sock, server.get_address())
                            display_path = get_remote_path(sock, server.get_address())
                            is_client_shell = False
                            threading.Thread(target=shared_shell_receive_loop, args=(sock,)).start()
                            continue
                        else:  # private remote shell
                            if cd_server == server:
                                is_client_shell = False  # switch to remote shell
                                display_path = server.base_path
                    else:
                        print("Invalid Command - Use 'mount private host:port:path' first to mount remote shell")
                else:  # normal client cd
                    try:
                        os.chdir(cd_path)
                    except OSError:
                        print('Error changing directory on client')
                    display_path = os.getcwd()
                continue

            else:  # normal client terminal command
                print(subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout)
                continue

        else:  # remote shell
            if is_shared_shell:  # shared remote shell
                run_remote_shared_cmd(sock, server.get_address(), cmd)
                shared_shell_lock.acquire()
                shared_shell_lock.release()
                continue

            else:  # private remote shell
                if len(cmd_lst) == 2 and cmd_lst[0] == 'cd':  # private remote shell cd
                    cd_path = cmd_lst[1]
                    remote_path = os.path.normpath(os.path.join(display_path, cd_path))
                    if is_child_path(server.base_path, remote_path):
                        if valid_remote_path(sock, server.get_address(), remote_path):
                            display_path = remote_path  # Update display path with valid remote path
                        else:
                            print('Error changing directory on remote shell')
                    else:  # cd outside of remote
                        is_client_shell = True
                        try:
                            os.chdir(cd_path)
                        except OSError:
                            print('Error changing directory on client')
                        display_path = os.getcwd()
                    continue

                elif len(cmd_lst) == 3 and cmd_lst[0] == 'cp':  # example: cp a.txt cwd
                    filename = cmd_lst[1]
                    path_local = '.' if cmd_lst[2] == 'cwd' else cmd_lst[2]
                    file_path_remote = os.path.normpath(os.path.join(display_path, filename))
                    remote_copy_file(sock, server.get_address(), file_path_remote, path_local, filename)
                    continue

                else:  # normal remote shell command
                    print(run_remote_cmd(sock, server.get_address(), cmd, display_path))
                    continue
