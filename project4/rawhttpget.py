#!/usr/bin/env python

#def ipheader():


#def tcpheader():


#def checksum():


def main():
    #get the target url
    url = sys.argv[1]

    #handle url exceptiongs, only slash, etc

    #create socket

    #socket.gethostbyname(), and select correct localhost

    #build and send the first packet

    #three-way handshake?

    #enter a receiving while loop, sending acks
        #timeout, out-of-order, duplication, congestion (cwnd max 1000)

    #connection teardown?


if __name__ == "__main__":
    main()
