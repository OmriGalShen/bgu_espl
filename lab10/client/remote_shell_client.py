import random
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path, PurePath
from typing import Optional

from client.network_helper import *


# To run on linux:
# mount private 192.168.56.1:500:/Server
# cd 192.168.56.1:500:/Server

# To run on both windows and linux:
# mount shared 192.168.56.1:500:Server
# mount private 192.168.56.1:500:Server
# cd 192.168.56.1:500:Server


class ServerInfo:
    def __init__(self, host_ip, port, base_path):
        self.base_path = base_path
        self.port = int(port)
        self.host_ip = host_ip

    def __eq__(self, other):
        return self.host_ip == other.host_ip and self.port == other.port and self.base_path == other.base_path

    def get_address(self):
        return self.host_ip, self.port


display_path = os.getcwd()
is_mounted = False
is_shared_shell = False
server: Optional[ServerInfo] = None
udp_client_socket = None
udp_shared_shell_socket = None
is_client_shell = True
client_address = None
wait_for_shared = False


def cd_on_client(path):
    global display_path
    try:
        os.chdir(path)
    except OSError:
        print('Error changing directory on client')
    display_path = os.getcwd()


def is_child_path(parent, child):
    return not Path(child).is_absolute() and PurePath(child).is_relative_to(parent)


def shared_shell_receive_loop(rec_sock, send_sock, address):
    global display_path, wait_for_shared
    while True:
        data, _ = rec_sock.recvfrom(BUFFER_SIZE)
        data = data.decode('utf-8')
        if len(data) > 0:
            print(f"{get_remote_path(send_sock, address)}$ ")
            print(data)
        wait_for_shared = False


def execute_command(cmd):
    global is_shared_shell, is_client_shell, server, is_mounted
    global display_path, udp_client_socket
    global udp_shared_shell_socket, wait_for_shared
    sock = udp_client_socket

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
            return

        if len(cmd_lst) == 3 and cmd_lst[0] == 'mount' \
                and cmd_lst[1] == 'shared':  # mount private host:port:path
            server = ServerInfo(*cmd_lst[2].split(':'))  # host_ip:port:path
            is_mounted = True
            is_shared_shell = True
            threading.Thread(target=shared_shell_receive_loop,
                             args=(udp_shared_shell_socket, udp_client_socket, server.get_address())).start()
            return

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
                        return
                    else:  # private remote shell
                        if cd_server == server:
                            is_client_shell = False  # switch to remote shell
                            display_path = server.base_path
                else:
                    print("Invalid Command - Use 'mount private host:port:path' first to mount remote shell")
            else:  # normal client cd
                cd_on_client(cd_path)
            return

        else:  # normal client terminal command
            print(subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout)
            return

    else:  # remote shell
        if is_shared_shell:  # shared remote shell
            run_remote_shared_cmd(sock, server.get_address(), cmd)
            wait_for_shared = True
            while wait_for_shared:
                time.sleep(0.5)
            display_path = get_remote_path(sock, server.get_address())
            return

        else:  # private remote shell
            if len(cmd_lst) == 2 and cmd_lst[0] == 'cd':
                cd_path = cmd_lst[1]
                remote_path = os.path.normpath(os.path.join(display_path, cd_path))
                if is_child_path(server.base_path, remote_path):
                    if valid_remote_path(sock, server.get_address(), remote_path):
                        display_path = remote_path  # Update display path with valid remote path
                    else:
                        print('Error changing directory on remote shell')
                else:  # cd outside of remote
                    is_client_shell = True
                    cd_on_client(cd_path)
                return

            elif len(cmd_lst) == 3 and cmd_lst[0] == 'cp':  # example: cp a.txt cwd
                filename = cmd_lst[1]
                path_local = '.' if cmd_lst[2] == 'cwd' else cmd_lst[2]
                file_path_remote = os.path.normpath(os.path.join(display_path, filename))
                remote_copy_file(sock, server.get_address(), file_path_remote, path_local, filename)
                return

            else:  # normal remote shell command
                print(run_remote_cmd(sock, server.get_address(), cmd, display_path))
                return


def open_socket():
    global udp_client_socket
    global udp_shared_shell_socket
    global client_address
    client_host = socket.gethostbyname(socket.gethostname())
    client_port = random.randint(6000, 10000)
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_shared_shell_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    client_address = (client_host, client_port)
    shared_shell_address = (client_host, client_port + 1)
    udp_client_socket.bind(client_address)
    udp_shared_shell_socket.bind(shared_shell_address)


if __name__ == '__main__':
    open_socket()
    while True:
        print(f"{display_path}$ ", end='')
        user_cmd = input()
        execute_command(user_cmd)
