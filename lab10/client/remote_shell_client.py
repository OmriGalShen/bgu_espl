import os
import random
import socket
import subprocess
import sys
import threading
from functools import wraps
from pathlib import Path, PurePath
import time

# To run on linux:
# mount private 192.168.56.1:500:/Server
# cd 192.168.56.1:500:/Server

# To run on both windows and linux:
# mount shared 192.168.56.1:500:Server
# mount private 192.168.56.1:500:Server
# cd 192.168.56.1:500:Server
BUFFER_SIZE = 1 << 10
shared_shell_listening = False


class ServerInfo:
    def __init__(self, host_ip, port, base_path):
        self.base_path = base_path
        self.port = int(port)
        self.host_ip = host_ip

    def __eq__(self, other):
        return self.host_ip == other.host_ip and self.port == other.port and self.base_path == other.base_path

    def get_address(self):
        return self.host_ip, self.port


def blocking_shared_shell(func):
    """used to decorate function  which received data from server
    in order to prevent losing data to shared command thread"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        global shared_shell_listening
        temp = shared_shell_listening
        shared_shell_listening = False
        result = func(*args, **kwargs)
        shared_shell_listening = temp
        return result

    return wrapper


@blocking_shared_shell
def remote_login(sock):
    data = "0"  # msg type 0 = remote_login
    sock.sendto(data.encode('utf-8'), mounted_server.get_address())
    status, _ = sock.recvfrom(BUFFER_SIZE)
    status = status.decode('utf-8')  # '0' = failed '1' successful
    return status == '1'


def remote_logout(sock):
    data = "1"  # msg type 1 = remote_logout
    sock.sendto(data.encode('utf-8'), mounted_server.get_address())


@blocking_shared_shell
def valid_remote_path(sock, path):
    data = f"2 {path}"  # msg type 2 = valid_remote_path
    sock.sendto(data.encode('utf-8'), mounted_server.get_address())
    status, _ = sock.recvfrom(BUFFER_SIZE)
    status = status.decode('utf-8')  # '0' = failed '1' successful
    return status == '1'


@blocking_shared_shell
def run_remote_cmd(sock, cmd, path):
    data = f"3 {path} {cmd}"  # msg type 3 = run_remote_cmd
    sock.sendto(data.encode('utf-8'), mounted_server.get_address())
    res, _ = sock.recvfrom(BUFFER_SIZE)
    res = res.decode('utf-8')
    return res


@blocking_shared_shell
def remote_copy_file(sock, remote_file_path, local_path, file_name):
    data = f"4 {remote_file_path}"  # msg type 4 = remote_copy_file
    sock.sendto(data.encode('utf-8'), mounted_server.get_address())
    status, _ = sock.recvfrom(BUFFER_SIZE)
    status = status.decode('utf-8')  # '0' = failed '1' successful
    if status == '1':
        local_file_path = os.path.normpath(os.path.join(local_path, file_name))
        f = open(local_file_path, 'wb')
        data, _ = sock.recvfrom(BUFFER_SIZE)
        try:
            while data:
                f.write(data)
                sock.settimeout(2)
                data, _ = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            f.close()
    else:
        print('Error: invalid remote file')


def share_cmd(sock, cmd):
    data = f"5 {cmd}"  # share_cmd
    sock.sendto(data.encode('utf-8'), mounted_server.get_address())


def cd_on_client():
    try:
        os.chdir(cd_path)
    except:
        print('Error changing directory on client')
    return os.getcwd()


def is_child_path(parent, child):
    return not Path(child).is_absolute() and PurePath(child).is_relative_to(parent)


def shared_shell_receive_loop(sock):
    global shared_shell_listening
    while True:
        if shared_shell_listening:
            data, _ = sock.recvfrom(BUFFER_SIZE)
            data = data.decode('utf-8')
            cmd = data.split(' ')
            print(subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout)
        else:  # wait for blocking to release
            time.sleep(0.5)


if __name__ == '__main__':
    is_mounted = False
    is_shared_shell = False
    mounted_server = None
    is_client_shell = True

    # Open socket
    client_ip = socket.gethostbyname(socket.gethostname())
    client_port = random.randint(6000, 10000)
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.bind((client_ip, client_port))

    display_path = os.getcwd()  # update with cwd

    while True:
        print(f"{display_path}$ ", end='')
        user_input = input()
        input_lst = user_input.split(' ')

        if user_input == 'quit' or user_input == 'exit':  # exit condition
            if is_shared_shell:
                remote_logout(UDPClientSocket)
            sys.exit()

        if is_client_shell:

            if len(input_lst) == 3 and input_lst[0] == 'mount' \
                    and input_lst[1] == 'private':  # mount private host:port:path
                mounted_server = ServerInfo(*input_lst[2].split(':'))  # host_ip:port:path
                if valid_remote_path(UDPClientSocket, mounted_server.base_path) is True:
                    is_mounted = True
                else:
                    mounted_server = None
                    is_mounted = False
                    print('Invalid remote remote shell')
                continue

            if len(input_lst) == 3 and input_lst[0] == 'mount' \
                    and input_lst[1] == 'shared':  # mount private host:port:path
                mounted_server = ServerInfo(*input_lst[2].split(':'))  # host_ip:port:path
                if valid_remote_path(UDPClientSocket, mounted_server.base_path) is True:
                    if remote_login(UDPClientSocket) is True:
                        is_mounted = True
                        is_shared_shell = True
                        shared_shell_listening = True
                        print("client_port:" + str(client_port))
                        threading.Thread(target=shared_shell_receive_loop, args=(UDPClientSocket,)).start()
                        continue
                mounted_server = None
                is_mounted = False
                print('Error: invalid remote shell')
                continue

            elif input_lst[0] == 'cd' and len(input_lst) == 2:  # cd command on client
                cd_path = input_lst[1]
                cd_path_lst = cd_path.split(':')
                if is_mounted and len(cd_path_lst) == 3:  # cd host:port:path
                    cd_server = ServerInfo(*cd_path_lst)
                    if cd_server == mounted_server:
                        is_client_shell = False  # switch to remote terminal
                        display_path = mounted_server.base_path
                    else:
                        print("Invalid Command - Use 'mount private host:port:path' first to mount remote shell")
                else:  # normal client cd
                    display_path = cd_on_client()
                continue

            else:  # normal client terminal command
                if is_shared_shell:
                    share_cmd(UDPClientSocket, user_input)
                print(subprocess.run(user_input, capture_output=True, text=True, shell=True).stdout)
                continue

        else:  # remote terminal
            if len(input_lst) == 2 and input_lst[0] == 'cd':
                cd_path = input_lst[1]
                remote_path = os.path.normpath(os.path.join(display_path, cd_path))
                if is_child_path(mounted_server.base_path, remote_path):
                    if valid_remote_path(UDPClientSocket, remote_path):
                        display_path = remote_path  # Update display path with valid remote path
                    else:
                        print('Error changing directory on remote shell')
                else:  # cd outside of remote
                    is_client_shell = True
                    display_path = cd_on_client()
                continue

            elif len(input_lst) == 3 and input_lst[0] == 'cp':  # example: cp a.txt cwd
                filename = input_lst[1]
                path_local = '.' if input_lst[2] == 'cwd' else input_lst[2]
                file_path_remote = os.path.normpath(os.path.join(display_path, filename))
                remote_copy_file(UDPClientSocket, file_path_remote, path_local, filename)
                continue

            else:  # normal remote terminal command
                print(run_remote_cmd(UDPClientSocket, user_input, display_path))
                continue
