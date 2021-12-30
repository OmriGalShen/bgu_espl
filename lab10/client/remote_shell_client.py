import random
import socket
import subprocess
import sys
import threading
from functools import wraps
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


shared_shell_listening = False
display_path = os.getcwd()
is_mounted = False
is_shared_shell = False
server: Optional[ServerInfo] = None
udp_client_socket = None
is_client_shell = True


def blocking_shared_shell(func):
    """used to decorate function  which received data from server
    in order to prevent losing data to shared command thread"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        global shared_shell_listening
        shared_shell_listening = False
        result = func(*args, **kwargs)
        shared_shell_listening = True
        return result

    return wrapper


def cd_on_client(path):
    try:
        os.chdir(path)
    except OSError:
        print('Error changing directory on client')
    return os.getcwd()


def is_child_path(parent, child):
    return not Path(child).is_absolute() and PurePath(child).is_relative_to(parent)


def shared_shell_receive_loop(sock):
    global shared_shell_listening, is_shared_shell
    while True:
        if shared_shell_listening and is_shared_shell:
            data, _ = sock.recvfrom(BUFFER_SIZE)
            data = data.decode('utf-8')
            execute_command(data)


def execute_command(cmd):
    global is_shared_shell, is_client_shell, server, is_mounted
    global shared_shell_listening, display_path, udp_client_socket
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
            if valid_remote_path(sock, server.get_address(), server.base_path) is True:
                if remote_login(sock, server.get_address()) is True:
                    is_mounted = True
                    is_shared_shell = True
                    shared_shell_listening = True
                    threading.Thread(target=shared_shell_receive_loop, args=(sock,)).start()
                    return
            server = None
            is_mounted = False
            print('Error: invalid remote shell')
            return

        elif cmd_lst[0] == 'cd' and len(cmd_lst) == 2:  # cd command on client
            cd_path = cmd_lst[1]
            cd_path_lst = cd_path.split(':')
            if is_mounted and len(cd_path_lst) == 3:  # cd host:port:path
                cd_server = ServerInfo(*cd_path_lst)
                if cd_server == server:
                    is_client_shell = False  # switch to remote shell
                    display_path = server.base_path
                else:
                    print("Invalid Command - Use 'mount private host:port:path' first to mount remote shell")
            else:  # normal client cd
                display_path = cd_on_client(cd_path)
            return

        else:  # normal client terminal command
            print(subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout)
            return

    else:  # remote shell
        if is_shared_shell:
            share_cmd(sock, server.get_address(), cmd)

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
                display_path = cd_on_client(cd_path)
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
    client_ip = socket.gethostbyname(socket.gethostname())
    client_port = random.randint(6000, 10000)
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_client_socket.bind((client_ip, client_port))
    return udp_client_socket


if __name__ == '__main__':
    open_socket()
    while True:
        print(f"{display_path}$ ", end='')
        user_cmd = input()
        execute_command(user_cmd)
