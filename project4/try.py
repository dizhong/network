# raw sockets on Linux

import socket, sys, time, random
from struct import *
import netifaces as ni
import try_helper as h


# has_http is a true or false field, indicating whether this is the 1 http req
def send(addr, content, has_http):
    return;


def recv():
    chunk = b''

    return;



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
    ip_counter = 0


    # include ip header in received packets? protocol not available
    #s_recv.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # make ip and tcp header for handshake, don't fragment
    # TODO double check the parameters passed in
    syn = 1
    ack = 0
    fin = 0
    ip_h = h.ip_header(0, source_ip, dest_ip)
    tcp_h = h.tcp_header(source_port, 255, 0, 200, source_ip, dest_ip, b'', syn, ack, fin)

    # how do i do the 1 minute wait? just block for max 1 minute?
    # three-way handshake
    syn_packet = ip_h + tcp_h
    s_send.sendto(syn_packet, (dest_ip, 80))

    # receive syn/ack, uhhhhh
    # recv the ip version + header length uhh... byte?
    chunk = s_recv.recv(1000)
    byte = chunk[0]
    ver = byte >> 4
    ip_len = (byte & 15) * 4
    print(str(ver) + ' ' + str(ip_len))

    if len(chunk) >= ip_len:
        ip_header = chunk[0:ip_len]
        chunk = chunk[ip_len:]
        total_len = h.ip_processing(ip_header)
        check_checksum = h.checksum(ip_header)
        print(check_checksum)
        print("above checksum")
    else:
        print("ip header processing--need code to read more")

    # if correct, go on to recv the tcp header in a similar way
    # but we're gonna ignore the options and just read in 24 bytes first
    if len(chunk) >= 24:
        tcp_partial_header = chunk[0:24]
        chunk = chunk[24:]
        seq_n, ack_n, tcp_len = h.tcp_processing(tcp_partial_header)
        if tcp_len > 24:
            chunk = chunk[tcp_len-24:]
    else:
        print("tcp header processing--need code to read more")

    # probs no body to recv atm; skip this
    # send ack_packet
    syn = 0
    ack = 1
    fin = 0
    ip_h = h.ip_header(1, source_ip, dest_ip)
    tcp_h = h.tcp_header(source_port, ack_n, seq_n+1, 200, source_ip, dest_ip, b'', syn, ack, fin)
    ack_packet = ip_h + tcp_h
    s_send.sendto(ack_packet, (dest_ip, 80))

    # nothing to receive here
    # send http request, uhhh what should be my receiver window
    syn = 0
    ack = 0
    fin = 0
    ip_h = h.ip_header(2, source_ip, dest_ip)

    #http_body = sth
    #tcp_h = h.tcp_header(source_port, 0, seq_n+2+len(http_body), 200, source_ip, dest_ip, b'', syn, ack, fin)
    #request_pkt = ip_h + tcp_h + http_body
    

    # send fin packet


    # enter a receiving loop (write as i receive??) 
    # this will be a seperate function
        # block and wait for max 3 minute. if exceed, print error & sys.exit
        
        # make sure checksum looks right? this might be done in the tcp class?
        
        # oh. what about out-of-order packets. i guess i should discard the ones
        # already received and ignore the ones jumped to future?
        
        # construct and send ack?

        # one tcp packet corresponds to (one ip packet) or (multi ip fragments);
        # one http response might be broken into multiple tcp packets;
        # and there will likely be multiple http responses for one file? chunks
        # so perhaps some nested loops here?


    # close file and exit



if __name__ == "__main__":
    main()

