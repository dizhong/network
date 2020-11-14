import socket, sys, time, random
from struct import *
import netifaces as ni
import ip_handle as ip
import tcp_handle as tcp
import http_handle as http
import random
import time


class Connection():

    def __init__(self, source_ip, dest_ip, source_port, s_send, s_recv):
        self.sip = source_ip
        self.dip = dest_ip
        self.port = source_port

        self.ip_count = 0
        self.tcp_seq = random.randrange(500)
        self.tcp_ack = 0
        self.tcp_window = 200
        
        self.s_send = s_send
        self.s_recv = s_recv
        
        self.byte_buffer = b''
        self.recvsize = 4069


    # tcp_flags is a list of [syn, ack, fin]
    # data is http data in byte format
    # if any of the tcp flag is set, don't append data
    def send(self, tcp_flags, data):
        ip_h = ip.ip_header(self.ip_count, self.sip, self.dip)
        self.ip_count += 1
        tcp_h = tcp.tcp_header(self.port, self.tcp_seq, self.tcp_ack, self.tcp_window, self.sip, self.dip, data, tcp_flags)
        
        if tcp_flags['syn'] == 1:
            packet = ip_h + tcp_h
            self.tcp_seq = self.tcp_seq + 1
        else:
            packet = ip_h + tcp_h + data
            self.tcp_seq = self.tcp_seq + len(data)
            # does tcp header not consume any # in seq?

        self.s_send.sendto(packet, (self.dip, 80))
        
        return


    def sock_get_bytes(self, length):
        response = self.byte_buffer
        while (len(response) < length):
            try:
                self.s_recv.settimeout(60)
                chunk = self.s_recv.recv(self.recvsize)
            except socket.timeout:
                print("Exceeded 60 second timeout on socket recv. Exit process.")
                sys.exit()
            self.s_recv.settimeout(None)
            response += chunk
            if chunk == b'':
                return None
        self.byte_buffer = response[length:]
        return response[:length]
        
        
    def trim_buffer(self, length):
        trimmed = self.byte_buffer[:length]
        self.byte_buffer = self.byte_buffer[length:]
        return trimmed


    # tbvh i'm too sleepy to know what i'm doing anymore 
    # i think this returns a flag to say whether it successfully got a pkt
    # of the correct kind (and potentially seq #), so that 
    def check_pkt(self):
    
        ip_len_byte = self.sock_get_bytes(1)
        ip_len = (ip_len_byte[0] & 15) * 4

        ip_header = ip_len_byte + self.sock_get_bytes(ip_len - 1)
        total_len, correct_pkt = ip.ip_processing(ip_header, self.sip, self.dip)

        # if ip_processing tells us this is not a packet we want,
        # either from checksum or from source/destination ip,
        # trim the rest of pkt length from buffer and get out
        if not correct_pkt:
            trimmed = self.trim_buffer(total_len-ip_len)
            return False, trimmed

        # if correct, go on to recv the tcp header in a similar way
        # but we're gonna ignore the options and just read in 24 bytes first
        tcp_partial_header = self.sock_get_bytes(24)
        seq_n, ack_n, tcp_len, correct_pkt = tcp.tcp_processing(tcp_partial_header, self.port)

        #TODO logic for jumping out when incorrect and for updating seq ack
        if not correct_pkt:
            self.trim_buffer(total_len-ip_len-tcp_len)
            return False, trimmed
        
        self.tcp_ack = seq_n + 1
        trimmed = self.trim_buffer(total_len-ip_len-tcp_len)
        return True, trimmed


    # function to get http etc data from the correct pkt
    def recv(self):
        getting_pkt = False
        data = b''
        start_time = time.time()
        elapsed_time = 0
        counter = 0
        while((not getting_pkt) and (elapsed_time < 180)):
            getting_pkt, data = self.check_pkt()
            elapsed_time = time.time() - start_time
            counter = counter + 1
            
        if (elapsed_time >= 180):
            print("exiting program because wait time exceeds 3 minutes")
            sys.exit()
        
        print("after " + str(counter) + " got one?")
        return data
        
