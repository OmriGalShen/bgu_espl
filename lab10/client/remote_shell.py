import os
import random
import socket
import subprocess

DEFAULT_IP = '192.168.56.1'
DEFAULT_PORT = 500
# mount private 192.168.56.1:500:/Server
# cd 192.168.56.1:500:/Server
BUFFER_SIZE = 1 << 10


class ServerInfo:
    def __init__(self, host, port, host_path):
        self.host_path = host_path
        self.port = port
        self.host_ip = host

    def __eq__(self, other):
        return self.host_ip == other.host_ip and self.port == other.port and self.host_path == other.host_path

    def get_address(self):
        return self.host_ip, self.port


def change_remote_path(remote_path):
    data = f"0 {remote_path}"
    UDPClientSocket.sendto(data.encode('utf-8'), mounted_server.get_address())
    res_cd, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
    res_cd = res_cd.decode('utf-8').split(' ')
    is_changed = res_cd[0] == '1'  # '0' = failed '1' successful
    res_msg = ' '.join(res_cd[1:])  # remote path or potential failure message
    return is_changed, res_msg


def run_remote_cmd(cmd):
    data = f"1 {cmd}"
    UDPClientSocket.sendto(data.encode('utf-8'), mounted_server.get_address())
    res, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
    res = res.decode('utf-8')
    return res


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
                is_mounted = True
                continue

            elif input_lst[0] == 'cd' and len(input_lst) == 2:
                cd_path = input_lst[1]
                cd_path_lst = cd_path.split(':')
                if is_mounted and len(cd_path_lst) == 3:  # cd host:port:path
                    cd_server = ServerInfo(*cd_path_lst)
                    if mounted_server == cd_server:
                        is_cd_changed, cd_res_msg = change_remote_path(mounted_server.host_path)
                        if is_cd_changed:
                            remote_terminal = True
                            display_path = cd_res_msg
                        else:
                            print(cd_res_msg)  # print error
                        continue
                    else:
                        print("Invalid Command - Use 'mount private host:port:path' first to mount remote shell")
                else:  # normal client cd
                    try:
                        os.chdir(cd_path)
                        display_path = os.getcwd()  # update display path
                    except:
                        print('Error changing directory on client')
                    continue
            else:  # normal client terminal command
                print(subprocess.run(user_input, capture_output=True, text=True, shell=True).stdout)
                continue

        else:  # server terminal
            if input_lst[0] == 'cd' and len(input_lst) == 2:
                cd_path = input_lst[1]
                is_cd_changed, remote_msg = change_remote_path(cd_path)
                if is_cd_changed:
                    display_path = remote_msg
                else:  # if failed cd on remote return to client shell
                    try:
                        os.chdir(cd_path)
                        display_path = os.getcwd()  # update display path
                        remote_terminal = False  # return to client shell
                    except:
                        print('Error changing directory on client')
                continue
            else:  # normal remote terminal command
                print(run_remote_cmd(input_lst))
                continue
