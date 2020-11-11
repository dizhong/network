import socket, sys, time
from struct import *
import netifaces as ni


def main():

    # create a new recv socket with SOCK_STREAM/IPPROTO_IP
    try:
        s_recv = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except (socket.error, msg):
        print('RecvSock creation error. Code: ' + str(msg[0]) + msg[1])
        sys.exit()

    #s_recv.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    s_recv.bind((socket.gethostbyname(socket.gethostname()), 0))
    #s_recv.listen()
    s_recv.recvmsg(1028)



if __name__ == "__main__":
    main()


