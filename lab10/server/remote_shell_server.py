#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Omri and Pan
"""
import os
import pathlib
import socket
import subprocess
import threading
import queue
import sys
import sqlite3
from sqlite3 import Error

BUFFER_SIZE = 1 << 10
DEFAULT_IP = '192.168.56.1'
DEFAULT_PORT = 500
DATABASE_NAME = r"remote_shell.db"


# server Code
def receive_data(sock, packet_queue):
    while True:
        data, address = sock.recvfrom(BUFFER_SIZE)
        packet_queue.put((data, address))


def create_tables(database, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY AUTOINCREMENT, host TEXT NOT NULL, port INTEGER)''')
    # cur.execute('''CREATE TABLE IF NOT EXISTS groups
    #            (group_name text, user_addr INTEGER)''')
    database.commit()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def is_logged_in(cur, host, port):
    rows = cur.execute("SELECT id FROM users WHERE host = ? AND port=?",
                       (host, port)).fetchall()
    if rows:
        return True
    return False


def run_server(host):
    database = create_connection(DATABASE_NAME)
    cur = database.cursor()
    create_tables(database, cur)
    port = DEFAULT_PORT
    print('server hosting on IP-> ' + str(host))
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind((host, port))
    packet_queue = queue.Queue()

    os.chdir('Server')  # initial directory

    print('server Running...')

    threading.Thread(target=receive_data, args=(udp_server_socket, packet_queue)).start()
    while True:
        while not packet_queue.empty():
            data, client_address = packet_queue.get()
            client_host, client_port = client_address
            client_port = int(client_port)
            data = data.decode('utf-8')
            data = list(data.split(" "))
            msg_type = int(data[0])

            if msg_type == 0:  # remote_login
                try:
                    cur.execute("INSERT INTO users(host, port) VALUES(?,?)", (client_host, client_port))
                    database.commit()
                    status = "1".encode('utf-8')
                except sqlite3.Error:
                    status = "0".encode('utf-8')
                udp_server_socket.sendto(status, client_address)

            if msg_type == 1:  # remote_logout
                cur.execute("DELETE FROM users WHERE host=? AND port=?",
                            (client_host, client_port))
                database.commit()

            if msg_type == 2:  # valid_remote_path
                msg_path = data[1]
                parent_dir = pathlib.Path(__file__).parent.resolve()
                local_path = os.path.normpath(os.path.join(parent_dir, msg_path))
                if os.path.isdir(local_path):
                    status = "1".encode('utf-8')
                else:
                    status = "0".encode('utf-8')
                udp_server_socket.sendto(status, client_address)

            elif msg_type == 3:  # run_remote_cmd
                msg_path = data[1]
                parent_dir = pathlib.Path(__file__).parent.resolve()
                local_path = os.path.normpath(os.path.join(parent_dir, msg_path))
                print("HELLO: " + local_path)
                msg_cmd = data[2:]
                print('in run_remote_cmd')
                response = subprocess.run(msg_cmd, capture_output=True, text=True, shell=True, cwd=local_path).stdout
                print("response:" + response)
                response = response.encode('utf-8')
                udp_server_socket.sendto(response, client_address)
                print('done run_remote_cmd')

            elif msg_type == 4:  # remote_copy_file
                remote_file_path = data[1]
                parent_dir = pathlib.Path(__file__).parent.resolve()
                local_file_path = os.path.normpath(os.path.join(parent_dir, remote_file_path))

                if os.path.isfile(local_file_path):
                    status = '1'.encode('utf-8')
                    udp_server_socket.sendto(status, client_address)
                    f = open(local_file_path, "rb")
                    data = f.read(BUFFER_SIZE)
                    while data:
                        if udp_server_socket.sendto(data, client_address):
                            data = f.read(BUFFER_SIZE)
                else:
                    status = '0'.encode('utf-8')
                    udp_server_socket.sendto(status, client_address)

            elif msg_type == 5:  # get_remote_path
                parent_dir = pathlib.Path(__file__).parent.resolve()
                rel_path = os.path.relpath(os.getcwd(), start=parent_dir)
                rel_path = rel_path.encode('utf-8')
                udp_server_socket.sendto(rel_path, client_address)

            elif msg_type == 6:  # run_remote_shared_cmd
                cmd = ' '.join(data[1:])
                cd_cmd = data[1] == 'cd'
                if is_logged_in(cur, client_host, client_port):
                    if cd_cmd:
                        os.chdir(data[2])
                    parent_dir = pathlib.Path(__file__).parent.resolve()
                    rel_path = os.path.relpath(os.getcwd(), start=parent_dir)
                    first_msg = f"{rel_path} {cmd}"
                    print('first_msg:' + first_msg)
                    first_msg = first_msg.encode('utf-8')
                    if cd_cmd:
                        sec_msg = ""
                    else:
                        sec_msg = subprocess.run(cmd.split(' '), capture_output=True, text=True, shell=True).stdout
                    print('sec_msg:' + sec_msg)
                    sec_msg = sec_msg.encode('utf-8')

                    rows = cur.execute("SELECT host,port FROM users").fetchall()
                    for row in rows:
                        client_address = (row[0], int(row[1]))
                        udp_server_socket.sendto(first_msg, client_address)
                        udp_server_socket.sendto(sec_msg, client_address)
    udp_server_socket.close()
    database.close()


if __name__ == '__main__':
    server_ip = sys.argv[1]
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    run_server(server_ip)
