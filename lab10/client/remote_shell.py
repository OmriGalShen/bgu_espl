import os
import random
import subprocess
import socket

DEFAULT_IP = '192.168.56.1'
BUFFER_SIZE = 1 << 10


class ServerInfo:
    def __init__(self, host, port, host_path):
        self.host_path = host_path
        self.port = port
        self.host_ip = host

    def __eq__(self, other):
        return self.host_ip == other.host_ip and self.port == other.port and self.host_path == other.host_path

    def get_server(self):
        return self.host_ip, self.port


if __name__ == '__main__':
    is_mounted = False
    mounted_srv = None
    client_terminal = True

    client_ip = socket.gethostbyname(socket.gethostname())
    client_port = random.randint(6000, 10000)
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.bind((client_ip, client_port))

    path = os.getcwd()

    while True:
        print(f"{path}$ ", end='')
        user_input = input()
        input_lst = user_input.split(' ')

        if client_terminal:
            if user_input == 'quit':  # exit condition
                break

            if len(input_lst) == 3 \
                    and input_lst[0] == 'mount' \
                    and input_lst[1] == 'private':  # mount private host:port:path
                mounted_srv = ServerInfo(*input_lst[2].split(':'))  # host_ip:port:path
                is_mounted = True
                continue

            elif is_mounted \
                    and input_lst[0] == 'cd' \
                    and len(input_lst) == 2 \
                    and len(input_lst[1].split(':')) == 3:  # cd host:port:/path
                cd_server = ServerInfo(*input_lst[1].split(':'))  # host_ip:port:/Server
                if mounted_srv == cd_server:
                    data = f"0 {cd_server.host_path}"
                    UDPClientSocket.sendto(data.encode('utf-8'), mounted_srv.get_server())
                    data, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
                    path = data.decode('utf-8')  # get server's terminal path
                    server_terminal = True
                    continue
                else:
                    print("Invalid Command - Use 'mount private host:port:path' first to mount remote shell")
            else:
                exe_response = subprocess.run(input_lst, capture_output=True, text=True, shell=True).stdout
                print(exe_response)
                path = os.getcwd()  # path may have changed

        else:  # server terminal
            if input_lst[0] == 'cd':
                continue
            else:
                data = f"1 {user_input}"
                UDPClientSocket.sendto(data.encode('utf-8'), mounted_srv.get_server())
                data, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
                data = data.decode('utf-8').split(' ')  # get server's terminal path
                path, response = data[0], " ".join(data[1:])
                if len(response) > 0:
                    print(response)
