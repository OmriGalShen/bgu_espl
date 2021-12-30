#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Omri and Pan
"""
import os
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
DATABASE_NAME = r"remote_data.db"


# server Code
def receive_data(sock, packet_queue):
    while True:
        data, address = sock.recvfrom(BUFFER_SIZE)
        packet_queue.put((data, address))


def create_tables(database, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS users
               (user_name text, user_id INTEGER, adrr INTEGER)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS groups
               (group_name text, user_addr INTEGER)''')
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


def run_server(host):
    database = create_connection(DATABASE_NAME)
    cur = database.cursor()
    create_tables(database, cur)
    port = DEFAULT_PORT
    print('server hosting on IP-> ' + str(host))
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind((host, port))
    packet_queue = queue.Queue()

    print('server Running...')

    threading.Thread(target=receive_data, args=(udp_server_socket, packet_queue)).start()
    while True:
        while not packet_queue.empty():
            data, (msg_address, msg_port) = packet_queue.get()
            client_address = (msg_address, msg_port)
            data = data.decode('utf-8')
            data = list(data.split(" "))
            msg_type = data[0]

            if msg_type == '0':  # valid_remote_path
                msg_path = data[1]
                print('path got:' + msg_path)
                if os.path.isdir(msg_path):
                    response = "1"
                else:
                    response = "0"
                response = response.encode('utf-8')
                udp_server_socket.sendto(response, client_address)

            elif msg_type == '1':  # run_remote_cmd
                msg_path = data[1]
                msg_cmd = ' '.join(data[2:])
                response = subprocess.run(msg_cmd, capture_output=True, text=True, shell=True, cwd=msg_path).stdout
                response = response.encode('utf-8')
                udp_server_socket.sendto(response, client_address)

            elif msg_type == '2':  # remote_copy_file
                file_name = data[1]
                if os.path.isfile(file_name):
                    status = '1'.encode('utf-8')
                    udp_server_socket.sendto(status, client_address)
                    f = open(file_name, "rb")
                    data = f.read(BUFFER_SIZE)
                    while data:
                        if udp_server_socket.sendto(data, client_address):
                            data = f.read(BUFFER_SIZE)
                else:
                    status = '0'.encode('utf-8')
                    udp_server_socket.sendto(status, client_address)

    udp_server_socket.close()
    database.close()


# Serevr Code Ends Here


if __name__ == '__main__':
    server_ip = sys.argv[1]
    run_server(server_ip)
