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
    res, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
    res = res.decode('utf-8')
    is_valid = res == '1'  # '0' = failed '1' successful
    return is_valid


def run_remote_cmd(cmd, path):
    data = f"1 {path} {cmd} "
    UDPClientSocket.sendto(data.encode('utf-8'), mounted_server.get_address())
    res, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
    res = res.decode('utf-8')
    return res


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

    client_ip = socket.gethostbyname(socket.gethostname())
    client_port = random.randint(6000, 10000)
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.bind((client_ip, client_port))

    display_path = os.getcwd()

    while True:
        print(f"{display_path}$ ", end='')
        user_input = input()
        input_lst = user_input.split(' ')

        if client_terminal:
            if user_input == 'quit' or user_input == 'exit':  # exit condition
                break

            elif len(input_lst) == 3 and input_lst[0] == 'mount' \
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
                        client_terminal = False
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
            if input_lst[0] == 'cd' and len(input_lst) == 2:
                cd_path = input_lst[1]
                remote_path = os.path.normpath(os.path.join(display_path, cd_path))
                if is_child_path(mounted_server.base_path, remote_path):
                    if valid_remote_path(remote_path):
                        display_path = remote_path  # Update display path with valid remote path
                    else:
                        print('Error changing directory on remote shell')
                else:  # cd outside of remote
                    display_path = cd_on_client()
                continue

            else:  # normal remote terminal command
                print(run_remote_cmd(user_input, display_path))
                continue
