import socket, sys, time, random
from struct import *
import netifaces as ni


# calculating checksum
def checksum(msg):
    sumN = 0

    #loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        word = msg[i] + (msg[i+1]<<8)
        sumN = sumN + word

    # add the carry???
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


def ip_processing(ip_header, our_ip, server_ip):
    total_length = unpack('!H', ip_header[2:4])
    correct_flg = False

    # TODO check if source_ip and dest_ip is what we want,
    # notice that it is flipped from the source and dest we get
    addr = unpack('!4s4s', ip_header[12:20])
    source_addr = socket.inet_ntoa(addr[0])
    dest_addr = socket.inet_ntoa(addr[1])
    ip_ver = ip_header[0] >> 4

    # check the checksum
    c_sum = checksum(ip_header)

    if (source_addr == server_ip) and (dest_addr == our_ip) and (c_sum == 0) and (ip_ver == 4):
        correct_flg = True

    return total_length[0], correct_flg


