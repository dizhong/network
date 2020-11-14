import socket, sys, time, random
from struct import *
import netifaces as ni

# calculating checksum

def checksum(msg):
    sumN = 0

    # wtf is i+1 shifted LEFT for 8 bits
    for i in range(0, len(msg), 2):
        word = msg[i] + (msg[i+1]<<8)
        sumN = sumN + word

    # add the carry???
    sumN = (sumN>>16) + (sumN & 0xffff)
    sumN = sumN + (sumN>>16)

    #complement and mask to 4 byte short (huh??)
    sumN = ~sumN & 0xffff

    return sumN


def tcp_header(source_port, seq, ack_n, window, source_ip, dest_ip, data, flags):
    tcp_source = source_port
    tcp_dest = 80
    tcp_seq = seq
    if flags['ack'] == 0:
        tcp_ack_seq = 0
    else:
        tcp_ack_seq = ack_n
    tcp_doff = 5
    # tcp flags
    tcp_fin = flags['fin']
    tcp_syn = flags['syn']
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = flags['ack']
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
    
    if 1 in flags.values():
        psu_pkt = psu_h + tcp_header
    else:
        psu_pkt = psu_h + tcp_header + data

    tcp_check = checksum(psu_pkt)

    tcp_header = pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack('H', tcp_check) + pack('!H', tcp_urg_ptr)

    return tcp_header;


# i'm just gonna skip the options here cuz what do i use them for?
def tcp_processing(tcp_header, our_port):
    seq_num = unpack('!L', tcp_header[4:8])
    ack_num = unpack('!L', tcp_header[8:12])
    tcp_len = (tcp_header[12] >> 4) * 4
    print(tcp_len)

    port = unpack('!H', tcp_header[2:4])
    if our_port == port[0]:
        flag = True
    else:
        flag = False

    # TODO is there like a checksum thing i need to do here?

    return seq_num[0], ack_num[0], tcp_len, flag;


