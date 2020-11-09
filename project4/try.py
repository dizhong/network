# raw sockets on Linux

import socket, sys, time, random
from struct import *
import netifaces as ni

# calculating checksum

def checksum(msg):
    sumN = 0

    #loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        word = msg[i] + (msg[i+1] << 8)
        sumN = sumN + word

    sumN = (sumN>>16) + (sumN & 0xffff)
    sumN = sumN + (sumN>>16)

    #complement and mask to 4 byte short (huh??)
    sumN = ~sumN & 0xffff

    return sumN


def ip_header(ip_id, source_ip, dest_ip):
    ip_ver = 4
    ip_ihl = 5 
    ip_tos = 0
    ip_len = 0 # supposedly kernel fills this out?
    ip_id = ip_id  # think this should always be 0 here?
    # ip_flag = 0 included in ip_frag_off
    ip_frag_off = 0
    ip_ttl = 225
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0   #kernel again?
    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)

    # what is this??
    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    ip_header = pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

    return ip_header;


def tcp_header(source_port, seq, ack, window, source_ip, dest_ip, data):
    tcp_source = source_port
    tcp_dest = 80
    tcp_seq = seq
    tcp_ack_seq = ack
    tcp_doff = 5
    # tcp flags
    tcp_fin = 0
    tcp_syn = 1
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 0
    tcp_urg = 0
    tcp_window = socket.htons(window) #though what is that socket.htons() thing?
    tcp_check = 0
    tcp_urg_ptr = 0

    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
    tcp_header = pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)

    # fields for psudo ip header for calculating checksum
    source_address = socket.inet_aton(source_ip)
    dest_address = socket.inet_aton(dest_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)

    psu_h = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    psu_h = psu_h + tcp_header + data

    tcp_check = checksum(psu_h)

    tcp_header = pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack('H', tcp_check) + pack('!H', tcp_urg_ptr)

    return tcp_header;


def http_header(dest):
    return;

# has_http is a true or false field, indicating whether this is the 1 http req
def send(addr, content, has_http):
    return;


def recv():
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

    # create a new socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except (socket.error, msg):
        print('Socket could not be created. Error code: ' + str(msg[0]) + msg[1])
        sys.exit()

    # get source ip (seems hacky tho) (router replaces internal IP with ext)
    source_ip = ni.ifaddresses('ens33')[ni.AF_INET][0]['addr']

    # and find a valid port to send (just uses socket.bind) (should i do (('', 0))?)
    sock.bind((source_ip, 0)) 
    source_port = sock.getsockname()[1]

    # make ip and tcp header for handshake, don't fragment
    ip_h = ip_header(0, source_ip, dest_ip)
    tcp_h = tcp_header(source_port, 255, 0, 1, source_ip, dest_ip, b'')

    # how do i do the 1 minute wait? just block for max 1 minute?
    # three-way handshake
    syn_packet = ip_h + tcp_h
    sock.sendto(syn_packet, (dest_ip, 80))

    # receive syn/ack

    # send ack_packet

    # send http request, uhhh what should be my receiver window


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

