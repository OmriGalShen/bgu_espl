import os
import random
import socket
import subprocess
from pathlib import Path, PurePath

# To run on linux:
# mount private 192.168.56.1:500:/Server
# cd 192.168.56.1:500:/Server

# To run on both windows and linux:
# mount private 192.168.56.1:500:Server
# cd 192.168.56.1:500:Server
BUFFER_SIZE = 1 << 10


class ServerInfo:
    def __init__(self, host_ip, port, base_path):
        self.base_path = base_path
        self.port = int(port)
        self.host_ip = host_ip

    def __eq__(self, other):
        return self.host_ip == other.host_ip and self.port == other.port and self.base_path == other.base_path

    def get_address(self):
        return self.host_ip, self.port


def valid_remote_path(path):
    data = f"0 {path}"
    UDPClientSocket.sendto(data.encode('utf-8'), mounted_server.get_address())
    status, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
    status = status.decode('utf-8')  # '0' = failed '1' successful
    is_valid = status == '1'
    return is_valid


def run_remote_cmd(cmd, path):
    data = f"1 {path} {cmd}"
    UDPClientSocket.sendto(data.encode('utf-8'), mounted_server.get_address())
    res, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
    res = res.decode('utf-8')
    return res


def remote_copy_file(remote_file_path, local_path,file_name):
    data = f"2 {remote_file_path}"
    UDPClientSocket.sendto(data.encode('utf-8'), mounted_server.get_address())
    status, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
    status = status.decode('utf-8')  # '0' = failed '1' successful
    if status == '1':
        local_file_path = os.path.normpath(os.path.join(local_path, file_name))
        f = open(local_file_path, 'wb')
        data, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
        try:
            while data:
                f.write(data)
                UDPClientSocket.settimeout(2)
                data, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            f.close()
    else:
        print('Error: invalid remote file')


def cd_on_client():
    try:
        os.chdir(cd_path)
    except:
        print('Error changing directory on client')
    return os.getcwd()


def is_child_path(parent, child):
    return not Path(child).is_absolute() and PurePath(child).is_relative_to(parent)


if __name__ == '__main__':
    is_mounted = False
    mounted_server = None
    client_terminal = True

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
            break

        if client_terminal:
            if len(input_lst) == 3 and input_lst[0] == 'mount' \
                    and input_lst[1] == 'private':  # mount private host:port:path
                mounted_server = ServerInfo(*input_lst[2].split(':'))  # host_ip:port:path
                if valid_remote_path(mounted_server.base_path) is True:
                    is_mounted = True
                else:
                    mounted_server = None
                    print('Invalid remote remote shell')
                continue

            elif input_lst[0] == 'cd' and len(input_lst) == 2:
                cd_path = input_lst[1]
                cd_path_lst = cd_path.split(':')
                if is_mounted and len(cd_path_lst) == 3:  # cd host:port:path
                    cd_server = ServerInfo(*cd_path_lst)
                    if cd_server == mounted_server:
                        client_terminal = False  # switch to remote terminal
                        display_path = mounted_server.base_path
                    else:
                        print("Invalid Command - Use 'mount private host:port:path' first to mount remote shell")
                else:  # normal client cd
                    display_path = cd_on_client()
                continue

            else:  # normal client terminal command
                print(subprocess.run(user_input, capture_output=True, text=True, shell=True).stdout)
                continue

        else:  # remote terminal
            if len(input_lst) == 2 and input_lst[0] == 'cd':
                cd_path = input_lst[1]
                remote_path = os.path.normpath(os.path.join(display_path, cd_path))
                if is_child_path(mounted_server.base_path, remote_path):
                    if valid_remote_path(remote_path):
                        display_path = remote_path  # Update display path with valid remote path
                    else:
                        print('Error changing directory on remote shell')
                else:  # cd outside of remote
                    client_terminal = True
                    display_path = cd_on_client()
                continue

            elif len(input_lst) == 3 and input_lst[0] == 'cp':  # example: cp a.txt cwd
                filename = input_lst[1]
                path_local = '.' if input_lst[2] == 'cwd' else input_lst[2]
                file_path_remote = os.path.normpath(os.path.join(display_path, filename))
                remote_copy_file(file_path_remote, path_local, filename)

            else:  # normal remote terminal command
                print(run_remote_cmd(user_input, display_path))
                continue
