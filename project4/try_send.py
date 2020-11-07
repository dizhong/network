# this is purely for sending a packet and checking if it looks right on wireshark

import socket, sys, time
from struct import *
import netifaces as ni

def checksum(msg):
    s = 0
    
    # why shift 8????
    for i in range(0, len(msg), 2):
        w = msg[i] + (msg[i+1] << 8)
        s = s + w

    # why shift 16??? oh and this is shifting on a different direction too
    s = (s>>16) + (s & 0xffff)
    # hmmm and then there is more shifting of 16
    s = s + (s >> 16)

    # and wtf is that squiggly line lolol
    s = ~s & 0xffff
    
    return s


def main():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except (socket.error, msg):
        print('Socket could not be created. Error Code: ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    packet = ''
    source_ip = ni.ifaddresses('ens33')[ni.AF_INET][0]['addr']
    s.bind((source_ip, 0))
    source_port = s.getsockname()[1]
    dest_ip = socket.gethostbyname('david.choffnes.com')
    print(dest_ip)

    # ip header fields
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0
    # need to look up again whats the diff between ip_id and ip_frag_off
    ip_id = 0
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)

    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    ip_header = pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

    # tcp header fields
    tcp_source = source_port
    tcp_dest = 80
    tcp_seq = 454
    tcp_ack_seq = 0
    tcp_doff = 5
    # tcp flags
    tcp_fin = 0
    tcp_syn = 1
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 0
    tcp_urg = 0
    tcp_window = socket.htons(5840)
    tcp_check = 0
    tcp_urg_ptr = 0

    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

    tcp_header = pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)

    # guess at 1 point this would be a http request... or a request split into 1000 par
    #user_data = 'hellow, how are you'

    # fields for psudo ip header for calculating checksum
    source_address = socket.inet_aton(source_ip)
    dest_address = socket.inet_aton(dest_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)

    psu_h = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    # wait, user data is counted too? oh right its the checksum of entire thing
    psu_h = psu_h + tcp_header

    tcp_check = checksum(psu_h)
    print(tcp_check)

    tcp_header = pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack('H', tcp_check) + pack('!H', tcp_urg_ptr)

    packet = ip_header + tcp_header

    count = 3

    for i in range(count):
        print('sending packet... ')
        s.sendto(packet, (dest_ip, 80))
        print('send')
        time.sleep(1)

    print('all packets send')



if __name__ == "__main__":
    main()




