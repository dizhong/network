import socket, sys, time, random
from struct import *
import netifaces as ni
import ip_handle as ip
import tcp_handle as tcp
import http_handle as http
import random


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
        tcp_h = tcp.tcp_header(self.port, self.tcp_seq, self.tcp_ack, self.tcp_window, self.sip, self.dip, data, tcp_flags)
        
        if 1 in tcp_flags:
            packet = ip_h + tcp_h
        else:
            packet = ip_h + tcp_h + data

        self.s_send.sendto(packet, (self.dip, 80))
        
        return


    def sock_get_bytes(self, length):
        response = self.byte_buffer
        while (len(response) < length):
            self.s_recv.settimeout(60)
            chunk = self.client.recv(self.bufsize)
            self.s_recv.settimeout(None)
            response += chunk
            if chunk == b'':
                return None
        self.byte_buffer = response[length:]
        return response[:length]

    # tbvh i'm too sleepy to know what i'm doing anymore 
    # i think this returns a flag to say whether it successfully got a pkt
    # of the correct kind (and potentially seq #), so that 
    def recv(self):
        chunk = self.byte_buffer

        self.s_recv.settimeout(60)
        chunk = chunk + self.s_recv.recv(1000)
        self.s_recv.settimeout(None)
        byte = chunk[0]
        ip_len = (byte & 15) * 4

        if len(chunk) >= ip_len:
            ip_header = chunk[0:ip_len]
            chunk = chunk[ip_len:]
            total_len, correct_pkt = ip.ip_processing(ip_header, self.sip, self.dip)
        else:
            print("ip header processing--need code to read more")

        # if ip_processing tells us this is not a packet we want,
        # either from checksum or from source/destination ip,
        # trim the rest of pkt length from buffer and get out
        if not correct_pkt:
            self.byte_buffer = chunk[total_len-ip_len:]
            return False;

        # if correct, go on to recv the tcp header in a similar way
        # but we're gonna ignore the options and just read in 24 bytes first
        if len(chunk) >= 24:
            tcp_partial_header = chunk[0:24]
            chunk = chunk[24:]
            seq_n, ack_n, tcp_len, correct_pkt = tcp.tcp_processing(tcp_partial_header, self.port)
            if tcp_len > 24:
                chunk = chunk[tcp_len-24:]
        else:
            print("tcp header processing--need code to read more")


        #TODO logic for jumping out when incorrect and for updating seq ack
        if correct_pkt:
            self.tcp_seq = ack_n
            self.tcp_ack = seq_n + 1
            self.byte_buffer = chunk
        else:
            self.byte_buffer = chunk[total_len-ip_len-tcp_len:]
            return False

        return True


    # a function to retreive received data?
    def data(self):
        return
        

