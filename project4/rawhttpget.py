#!/usr/bin python3
# raw sockets on Linux

import socket, sys, time, random
from struct import *
import netifaces as ni
from connection import Connection 
import ip, tcp, http


def create_connection(dest_ip):
    # create a new send socket with SOCK_RAW/IPPROTO_RAW
    try:
        s_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except (socket.error, msg):
        print('Socket could not be created. Error code:' + str(msg[0]) + msg[1])
        sys.exit()

    # create a new recv socket with SOCK_RAW/IPPROTO_IP
    try:
        s_recv = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except (socket.error, msg):
        print('RecvSock creation error. Code: ' + str(msg[0]) + msg[1])
        sys.exit()

    source_ip = ni.ifaddresses('ens33')[ni.AF_INET][0]['addr']
    # and find a valid port to send (just uses socket.connect)
    s_send.bind((source_ip, 0))
    source_port = s_send.getsockname()[1]

    conn = Connection(source_ip, dest_ip, source_port, s_send, s_recv)

    return conn


def main():
    # get download url from args and get ip and split out/create file name
    dest_url = sys.argv[1]
    website = dest_url.split("//")[1].split("/")[0]
    dest_ip = socket.gethostbyname(website)
    file_name = dest_url.split("//")[1].split("/")[-1]
    if file_name == '':
        file_name = 'index.html'
    print(file_name + " is file name\n")

    # create a new send socket with SOCK_RAW/IPPROTO_RAW
    #try:
    #    s_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    #except (socket.error, msg):
    #    print('Socket could not be created. Error code:' + str(msg[0]) + msg[1])
    #    sys.exit()

    # create a new recv socket with SOCK_RAW/IPPROTO_IP
    #try:
    #    s_recv = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    #except (socket.error, msg):
    #    print('RecvSock creation error. Code: ' + str(msg[0]) + msg[1])
    #    sys.exit()


    #source_ip = ni.ifaddresses('ens33')[ni.AF_INET][0]['addr']
    # and find a valid port to send (just uses socket.connect)
    #s_send.bind((source_ip, 0)) 
    #source_port = s_send.getsockname()[1]

    conn = create_connection(dest_ip)

    


if __name__ == "__main__":
    main()
