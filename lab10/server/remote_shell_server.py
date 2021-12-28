#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Omri and Pan
"""
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


def run_server(host):
    database = create_connection(DATABASE_NAME)
    cur = database.cursor()
    create_tables(database, cur)
    # host_ip = socket.gethostbyname(socket.gethostname())
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
                user_name = data[1]
                user_id = data[2]
                cur.execute("INSERT INTO users (user_name, user_id, adrr) VALUES(?,?,?)",
                            (user_name, user_id, msg_port))
                database.commit()
                response = "SERVER: Done".encode('utf-8')
                udp_server_socket.sendto(response, full_address)

            elif msg_type == '1':  # remove user
                cur.execute("DELETE FROM users WHERE adrr = ?", (msg_port,))
                database.commit()
                response = "SERVER: Done"
                udp_server_socket.sendto(response.encode('utf-8'), full_address)

            elif msg_type == '2':  # connect to group
                group_name = data[1]
                rows = []
                rows = cur.execute("SELECT group_name, user_addr FROM groups WHERE group_name = ?",
                                   (group_name,), ).fetchall()
                if not rows:
                    cur.execute("INSERT INTO groups (group_name, user_addr) VALUES(?,?)", (group_name, msg_port))
                    database.commit()
                if rows:
                    print("hereeee22")
                    print(rows)
                    print(type(rows))
                    user_exist = False
                    for index, row in enumerate(rows):
                        if row[1] == msg_port:
                            user_exist = True
                    if user_exist:
                        cur.execute("INSERT INTO groups (group_name, user_addr) VALUES(?,?)", (group_name, msg_port))
                        database.commit()
                response = "SERVER: Done".encode('utf-8')
                udp_server_socket.sendto(response, full_address)

            elif msg_type == '3':  # disconnect from group
                group_name = data[1]
                rows = cur.execute("SELECT group_name, user_addr FROM groups WHERE group_name = ?",
                                   (group_name,), ).fetchall()
                if not rows:
                    response = "SERVER: Group name does not exist".encode('utf-8')
                    udp_server_socket.sendto(response, full_address)
                else:
                    for index, row in enumerate(rows):
                        if row[1] == msg_port:
                            cur.execute("DELETE FROM groups WHERE user_addr = ?", (msg_port,))
                            database.commit()
                            response = "SERVER: Done".encode('utf-8')
                            udp_server_socket.sendto(response, full_address)

            elif msg_type == '4':  # send message to user
                user_name = data[1]
                rows = cur.execute("SELECT adrr FROM users WHERE user_name = ?", (user_name,), ).fetchall()
                user_ports = list(rows[0])
                send_address = (msg_port, user_ports[0])
                msg = ' '.join(data[2:]).encode('utf-8')
                udp_server_socket.sendto(msg, send_address)
                response = "SERVER: Done".encode('utf-8')
                udp_server_socket.sendto(response, full_address)

            elif msg_type == '5':  # send message to group
                group_name = data[1]
                print("im here now")
                rows = cur.execute("SELECT user_addr FROM groups WHERE group_name = ?", (group_name,), ).fetchall()
                print("rows")
                user_ports = list(sum(rows, ()))  # convert tuple of tuples to list
                print(user_ports)
                print(type(user_ports[0]))
                print(type(rows[0]))
                send_address = (msg_address, user_ports[0])
                msg = ' '.join(data[2:]).encode('utf-8')
                if msg_port in user_ports:
                    for user_port in user_ports:
                        if user_port != msg_port:
                            send_address = (msg_address, user_port)
                            udp_server_socket.sendto(msg, send_address)
                    response = "SERVER: Done".encode('utf-8')
                else:
                    response = "SERVER: Your not in the group, please join first".encode('utf-8')
                udp_server_socket.sendto(response, full_address)
    udp_server_socket.close()
    database.close()


# Serevr Code Ends Here


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


if __name__ == '__main__':
    server_ip = sys.argv[1]
    run_server(server_ip)
