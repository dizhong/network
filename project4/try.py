# raw sockets on Linux

import socket, sys, time, random
from struct import *
import netifaces as ni

# calculating checksum

def checksum(msg):
    sumN = 0

    #loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        word = ord(msg[i]) + (ord(msg[i+1]) << 8)
        sumN = sumN + word

    sumN = (sumN>>16) + (sumN & 0xffff)
    sumN = sumN + (sumN>>16)

    #complement and mask to 4 byte short (huh??)
    sumN = ~sumN & 0xffff

    return sumN


def ip_header(ip_id, source_ip, dest_ip):
    ip_ihl = 5 # what are these again??
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0
    ip_id = ip_id
    ip_frag_off = 0
    ip_ttl = 225
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)

    # what is this??
    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    ip_header = pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_grag_off, ip_tto, ip_proto, ip_check, ip_saddr, ip_daddr)

    return ip_header;


def tcp_header(source, seq, ack, window):
    tcp_source = source
    tcp_dest = 80
    tcp_seq = seq
    tcp_ack = ack
    tcp_urg = 0
    tcp_window = window #though what is that socket.htons() thing?
    tcp_urg_ptr = 0

    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
    tcp_header = pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)

    return tcp_header;


def http_header(dest):
    return header;


def send(addr, content):



def recv():




def main():
    # get download url from args and get ip and split out/create file name
    dest_url = sys.argv[1]
    dest_ip = socket.gethostbyname(dest_url)
    file_name = dest_url.split("//")[1].split("/")[-1]
    if file_name == '':
        file_name = 'index.html'
    print(file_name + " is file name\n")

    # create a new socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except socket.error, msg:
        print('Socket could not be created. Error code: ' + str(msg[0]) + msg[1])
        sys.exit()

    # use system's dns resolver to get the ip address???
    dest_ip = socket.gethostbyname(dest_url)

    # get source ip (seems hacky tho) (router replaces internal IP with ext)
    source_ip = ni.ifaddresses('ens33')[ni.AF_INET][0]['addr']

    # and find a valid port to send (just uses socket.bind) (should i do (('', 0))?)
    sock.bind((source_ip, 0)) 

    # make ip and tcp header for handshake, don't fragment
    ip_h = ip_header(0, source_ip, dest_ip)

    # how do i do the 1 minute wait? just block for max 1 minute?
    # three-way handshake


    # send request, uhhh what should be my receiver window


    # client side connection teardown


    # enter a receiving loop (write as i receive??) 
    # this will be a seperate function
        # block and wait for max 3 minute. if exceed, print error & sys.exit
        
        # make sure checksum looks right? this might be done in the tcp class?
        
        # oh. what about out-of-order packets. i guess i should discard the ones
        # already received and ignore the ones jumped to future?
        
        # construct and send ack?
    
        # notice that. one ip packets might be fragmented to multiple packets;
        # one tcp packet corresponds to (one ip packet) or (multi ip fragments);
        # one http response might be broken into multiple tcp packets;
        # and there will likely be multiple http responses for one file? chunks
        # so perhaps some nested loops here?


    # close file and exit



if __name__ == "__main__":
    main()

