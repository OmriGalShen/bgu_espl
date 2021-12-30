import os
from socket import timeout

from remote_shell_client import blocking_shared_shell

BUFFER_SIZE = 1 << 10


@blocking_shared_shell
def remote_login(sock, address):
    data = "0"  # msg type 0 = remote_login
    sock.sendto(data.encode('utf-8'), address)
    status, _ = sock.recvfrom(BUFFER_SIZE)
    status = status.decode('utf-8')  # '0' = failed '1' successful
    return status == '1'


def remote_logout(sock, address):
    data = "1"  # msg type 1 = remote_logout
    sock.sendto(data.encode('utf-8'), address)


@blocking_shared_shell
def valid_remote_path(sock, address, path):
    data = f"2 {path}"  # msg type 2 = valid_remote_path
    sock.sendto(data.encode('utf-8'), address)
    status, _ = sock.recvfrom(BUFFER_SIZE)
    status = status.decode('utf-8')  # '0' = failed '1' successful
    return status == '1'


@blocking_shared_shell
def run_remote_cmd(sock, address, cmd, path):
    data = f"3 {path} {cmd}"  # msg type 3 = run_remote_cmd
    sock.sendto(data.encode('utf-8'), address)
    res, _ = sock.recvfrom(BUFFER_SIZE)
    res = res.decode('utf-8')
    return res


@blocking_shared_shell
def remote_copy_file(sock, address, remote_file_path, local_path, file_name):
    data = f"4 {remote_file_path}"  # msg type 4 = remote_copy_file
    sock.sendto(data.encode('utf-8'), address)
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
        except timeout:
            f.close()
    else:
        print('Error: invalid remote file')


def share_cmd(sock, address, cmd):
    data = f"5 {cmd}"  # share_cmd
    sock.sendto(data.encode('utf-8'), address)


