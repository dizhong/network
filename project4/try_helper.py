# helper functions for try.py... will probably be broken down even more in the future

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

    return ip_header


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


