import socket, sys, time, random
from struct import *
import netifaces as ni

# method for calculating checksum
def checksum(msg):
    sumN = 0

    #if len(msg) % 2 == 1:
    #    msg = msg + b'0'
    print(len(msg))
        
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

  
def http_get(request_url):
    request = "GET " + request_url + " HTTP/1.1\r\n"\
              "HOST: fring.ccs.neu.edu\r\n\r\n"
             #"Cookie:" + cookie + "\r\n\r\n"
             # "X-CSRFTOKEN:" + csrf + "\r\n\r\n"
    return request.encode()
    

def main():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except (socket.error, msg):
        print('Socket could not be created. Error Code: ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    # create a new recv socket with SOCK_RAW/IPPROTO_IP
    #try:
    s_recv = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    #except (socket.error, msg):
    #    print('RecvSock creation error. Code: ' + str(msg[0]) + msg[1])
    #    sys.exit()


    packet = ''
    source_ip = ni.ifaddresses('ens33')[ni.AF_INET][0]['addr']
    s.bind((source_ip, 0))
    source_port = s.getsockname()[1]
    dest_ip ='127.0.0.1'

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
    tcp_syn = 0
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 1
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
    
    request = http_get('david.choffines.com')
    if len(request) % 2 == 1:
        request = request + b'0'
    tcp_length = len(tcp_header) + len(request)

    psu_h = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    
    
    
    #request = b''
    psu_pkt = psu_h + tcp_header + request

    tcp_check = checksum(psu_pkt)
    #print(tcp_check)

    header = pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack('H', tcp_check) + pack('!H', tcp_urg_ptr)

    packet = ip_header + header + request

    s.sendto(packet, (dest_ip, 80))


    tcp_length = len(tcp_header)

    psu_h = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    psu_pkt2 = psu_h + tcp_header


    tcp_check2 = checksum(psu_pkt2)
    print(tcp_check2)

    tcp_header2 = pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack('H', tcp_check2) + pack('!H', tcp_urg_ptr)

    packet2 = ip_header + tcp_header2

    s.sendto(packet2, (dest_ip, 80))




if __name__ == "__main__":
    main()

