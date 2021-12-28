#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Omri and Pan
"""
import os
import socket
import threading
import queue
import sys
import sqlite3
from sqlite3 import Error

BUFFER_SIZE = 1 << 10
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
            full_address = (msg_address, msg_port)
            data = data.decode('utf-8')
            data = list(data.split(" "))
            msg_type = data[0]

            if msg_type == '0':  # new user
                msg_path = data[1]
                full_path = os.path.join(os.getcwd(), msg_path)
                response = f"{full_path}$ ".encode('utf-8')
                udp_server_socket.sendto(response, full_address)

            elif msg_type == '1':  # remove user
                cur.execute("DELETE FROM users WHERE adrr = ?", (msg_port,))
                database.commit()
                response = "SERVER: Done"
                udp_server_socket.sendto(response.encode('utf-8'), full_address)

            elif msg_type == '2':  # cd command
                cur.execute("DELETE FROM users WHERE adrr = ?", (msg_port,))
                database.commit()
                response = "SERVER: Done"
                udp_server_socket.sendto(response.encode('utf-8'), full_address)

    udp_server_socket.close()
    database.close()


# Serevr Code Ends Here


if __name__ == '__main__':
    server_ip = sys.argv[1]
    run_server(server_ip)
