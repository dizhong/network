
import socket, sys


#a class for reading in the response
class Read:
    def __init__(self, client):
        self.client = client
        self.byte_buffer = b''
        self.bufsize = 4069

    # For reading chunks with a known length
    def read_bytes(self, length):
        response = self.byte_buffer
        while (len(response) < length):
            chunk = self.client.recv(self.bufsize)
            response += chunk
            if chunk == b'':
                return None
        self.byte_buffer = response[length:]
        return response[:length]

    #for reading in header/chunked encoding lehgth field
    def read_until(self, suffix):
        response = self.byte_buffer
        while not (suffix in response):
            chunk = self.client.recv(self.bufsize)
            response += chunk
            if chunk == b'':
                return None
        split = response.split(suffix, 1)
        if len(split) > 1:
            self.byte_buffer = split[1]
        else:
            self.byte_buffer = b''
        return split[0] 
        
# get the response message 
# input: client
# output: String body, Dict parsed_header, String header
def get_message(client):
    read_message = Read(client)
    #get the header
    suffix = b'\r\n\r\n' 
    header = read_message.read_until(suffix)
    response = b''
    if header is None:
        return "", {'status':1000}, ""
    parsed_header = response_header_parse(header.decode())
    #print(header.decode())
    #get chunks in a loop
    if parsed_header['chunked'] == True:
        chunk = b''
        suffix = b'\r\n'
        length = True
        #length = read_message.read_until(suffix)
        while length != 0:
            length = read_message.read_until(suffix)
            if length is None:
                return "", {'status':1000}, ""
            elif length == b'':
                break;
            length = length.decode()
            length = length.split(";")[0]
            length = int(length, 16)
            chunk = read_message.read_bytes(length)
            response += chunk
            read_message.read_until(suffix)
            #print(str(length) + " length of chunk\n")
            #print(chunk.decode())
    else:
        response = read_message.read_bytes(parsed_header['length'])
    return response.decode(), parsed_header, header.decode()
    #get response when not chunked

