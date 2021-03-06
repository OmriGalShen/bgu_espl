import random
import socket
import subprocess
import sys
import threading
from pathlib import Path, PurePath

from client.network_helper import *


# How to run
# mount shared 192.168.56.1:500:/Server | mount private 192.168.56.1:500:/Server
# cd 192.168.56.1:500:/Server


class ServerInfo:
    def __init__(self, host_ip, port, base_path):
        if base_path[0] == '/':
            base_path = base_path[1:]
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
    global display_path, send_shared_cmd
    while True:
        res, _ = client_sock.recvfrom(BUFFER_SIZE)
        res = res.decode('utf-8').split(' ')
        rem_path = res[0]
        is_cd_cmd = res[1] == 'cd'
        rem_cmd = ' '.join(res[1:])
        old_path, new_path = display_path, rem_path
        res, _ = client_sock.recvfrom(BUFFER_SIZE)
        cmd_output = res.decode('utf-8')

        if not send_shared_cmd:  # received from another client
            print(rem_cmd)
            if len(cmd_output) > 0:
                print()
                print(cmd_output)
            print(f"/{new_path}$ ", end='')
        else:  # send from this client
            if len(cmd_output) > 0:
                print()
                print(cmd_output)
            print(f"/{new_path}$ ", end='')
        display_path = new_path  # update path
        send_shared_cmd = False
        barrier.wait()


if __name__ == '__main__':
    is_mounted = False
    is_shared_shell = False
    server = None
    is_client_shell = True
    send_shared_cmd = False
    display_path = os.getcwd()
    is_display_path = True

    client_host = socket.gethostbyname(socket.gethostname())
    client_port = random.randint(6000, 10000)
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.bind((client_host, client_port))

    barrier = threading.Barrier(1)

    while True:
        if is_display_path:
            print(f"/{display_path}$ ", end='')
        is_display_path = True
        cmd = input()
        barrier.reset()

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

            elif len(cmd_lst) == 3 and cmd_lst[0] == 'mount' \
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
                            continue
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
                send_shared_cmd = True
                is_display_path = False
                run_remote_shared_cmd(sock, server.get_address(), cmd)
                barrier.wait()  # wait for remote shared shell response
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
                    else:  # cd outside of remote shell
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
