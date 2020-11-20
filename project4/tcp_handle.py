import socket, sys, time, random
from struct import *
import netifaces as ni

# method for calculating checksum
def checksum(msg):
    sumN = 0
    
    if len(msg) % 2 == 1:
        msg = msg + b'\x00'
        
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

# method for constructing TCP header, given a lot of things
# returns a constructed TCP header
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
    tcp_length = len(tcp_header) + len(data)

    psu_h = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    
    #deciding whether to append data for checksum or this is a header-only packet
    #honestly not very useful, may be deletable
    #if flags[syn] == 1:
    #    psu_pkt = psu_h + tcp_header
    #else:
    psu_pkt = psu_h + tcp_header + data

    tcp_check = checksum(psu_pkt)

    tcp_header = pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack('H', tcp_check) + pack('!H', tcp_urg_ptr)

    return tcp_header;


# i'm just gonna skip the options here cuz what do i use them for?
# process the tcp header part of a captured packet, excluding options
# flag is for determining whether this is a packet we're looking for
def tcp_processing(tcp_header, our_port, current_ack, total_len, ip_len):
    seq_num = unpack('!L', tcp_header[4:8])
    ack_num = unpack('!L', tcp_header[8:12])
    tcp_len = (tcp_header[12] >> 4) * 4
    print(tcp_len)

    port = unpack('!H', tcp_header[2:4])
    
    # packet reordering and throw out duplicate packets?
    if (our_port == port[0]) and (seq_num[0] >= current_ack):
        correct_pkt = True
    else:
        correct_pkt = False
        
    # construct flags{is_ack:T/F, is_fin:T/F}
    recv_flags = {'is_ack':False, 'is_fin':False}
    tcp_flags = tcp_header[13]
    fin = tcp_flags & 1
    syn = (tcp_flags >> 1) & 1
    rst = (tcp_flags >> 2) & 1
    psh = (tcp_flags >> 3) & 1
    ack = (tcp_flags >> 4) & 1
    
    # uh actually retransmit...? uh what if only header too sleepy fuck life
    if ((ip_len + tcp_len) == total_len) and (syn != 1):
        recv_flags['is_ack'] = True
    if fin == 1:
        recv_flags['is_fin'] = True

    # TODO is there like a checksum thing i need to do here?

    return seq_num[0], ack_num[0], tcp_len, correct_pkt, recv_flags;


