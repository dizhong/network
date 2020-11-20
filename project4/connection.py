import socket, sys, time, random
from struct import *
import netifaces as ni
import ip_handle as ip
import tcp_handle as tcp
import http_handle as http
import random
import time


class Connection():

    def __init__(self, source_ip, dest_ip, source_port, s_send, s_recv, f):
        self.sip = source_ip
        self.dip = dest_ip
        self.port = source_port

        self.ip_count = 0
        self.tcp_seq = random.randrange(500)
        self.tcp_ack = 0
        self.tcp_window = 200
        self.has_fin = False
        
        self.s_send = s_send
        self.s_recv = s_recv
        
        self.byte_buffer = b''
        self.recvsize = 4069
        self.f_handle = f


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
        #print(ip_len_byte)
        ip_len = (ip_len_byte[0] & 15) * 4
        #print(str(ip_len) + " this is length of ip header from check_pkt")
        ip_header = ip_len_byte + self.sock_get_bytes(ip_len - 1)
        total_len, correct_pkt_ip = ip.ip_processing(ip_header, self.sip, self.dip)
        #print(str(total_len) + " this is total_len fro check_pkt")

        # if correct, go on to recv the tcp header in a similar way
        # but we're gonna ignore the options and just read in 20 bytes first
        tcp_partial_header = self.sock_get_bytes(20)
        seq_n, ack_n, tcp_len, correct_pkt_tcp, flags = tcp.tcp_processing(tcp_partial_header, self.port, self.tcp_ack, total_len, ip_len)
        if (tcp_len > 20):
            self.trim_buffer(tcp_len-20)
        #print(str(tcp_len) + " this is tcp_len printed in check_pkt")
        #print(correct_pkt_ip)
        #print(correct_pkt_tcp)
        payload_len = total_len-ip_len-tcp_len
        #print("Sequence numbe: " + str(seq_n))
        #print("Payload length: " + str(payload_len))
        #print("below trimmed")
        #TODO logic for jumping out when incorrect and for updating seq ack
        if (not correct_pkt_ip) or (not correct_pkt_tcp):
            trimmed = self.trim_buffer(payload_len)
            #print(trimmed)
            #print(self.byte_buffer)
            return False, b'', None, seq_n, ack_n, payload_len
        else:
            trimmed = self.trim_buffer(payload_len)
            #print(trimmed)
            #print(self.byte_buffer)
            return True, trimmed, flags, seq_n, ack_n, payload_len



    # function to get http etc data from the correct pkt
    def recv_pkt(self, bufsize):
        self.recvsize = bufsize
    
        getting_pkt = False
        data = b''
        #recv_flags = {}
        start_time = time.time()
        elapsed_time = 0
        counter = 0
        while((not getting_pkt) and (elapsed_time < 180) and (len(data) <= 0)):
            getting_pkt, data, recv_flags, seq_n, ack_n, data_len = self.check_pkt()
            elapsed_time = time.time() - start_time
            counter = counter + 1
            
        if (elapsed_time >= 180):
            print("exiting program because wait time exceeds 3 minutes")
            sys.exit()

        # the only thing to not send ack for is ack only pkts i think
        # probably need a flag for getting fin to tell the main
        #print(recv_flags)
        #print("above recv_flags printed from recv")
        if (recv_flags['is_syn']):
            self.tcp_ack = seq_n + 1
            ack_flags = {'syn':0, 'ack':1, 'fin':0}
            self.send(ack_flags, b'')
        elif  (recv_flags['is_fin']):
            self.has_fin = True
            self.tcp_ack = seq_n + data_len + 1
            ack_flags = {'syn':0, 'ack':1, 'fin':0}
            self.send(ack_flags, b'')
        elif (not recv_flags['is_ack']):
            self.tcp_ack = seq_n + data_len
            ack_flags = {'syn':0, 'ack':1, 'fin':0}
            self.send(ack_flags, b'')
        
        #print("after " + str(counter) + " got one?")
        #print("Real payload length: " + str(len(data)) + "\n")
        return data
        
        
    # only use once 3-way handshake has been established
    # Return: Byte data (<= len(bufsize))
    #         if len(data) == 0: connection has received fin flag and there is
    #                            no more old data to send
    def recv(self, bufsize):
        chunk = b''
        while (len(chunk) == 0) and (self.has_fin != True):
            data = self.recv_pkt(bufsize)
            chunk += data
            
        self.f_handle.write(chunk)
        return chunk
        
        
        
    
    
        
