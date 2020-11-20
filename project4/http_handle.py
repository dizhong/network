
import socket, sys


#a class for reading in the response
class Read:
    def __init__(self, client):
        self.client = client
        self.byte_buffer = b''
        self.bufsize = 65536

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
            #if chunk is None:
            #    return response.decode(), {'status':1000}, ""
            response += chunk
            result_until = read_message.read_until(suffix)
            #print(str(length) + " supposed length of chunk\n")
            #print(str(len(chunk)) + " actual length of chunk\n")
            #print(result_until)
            #print(chunk.decode() + "\n\n\n\n\n\n\n\n\n")
    else:
        response = read_message.read_bytes(parsed_header['length'])
    return response, parsed_header, header.decode()
    #get response when not chunked

# split by \r\n into list, then split list[0] by space
# find status_num, then parse by different num
# param: String http_response_msg
# return: dict parsed_header(status_num, url, cookies, csrf, chunked, length)
def response_header_parse(header):
    #print(header)
    #print("printed response msg")
    if (header == "" or header == "0\r\n\r\n"):
        # if get in a non-sense header, report back that the socket connection 
        # is probably broken
        parsed_header = {'status': 1000}
        return parsed_header
  
    header = header.split("\r\n")
    try:
        status_num = int(header[0].split(" ")[1])
    except:
        # Handle the exception
        print(header)
    cookies = ""
    csrf = ""
    url = None
    length = 0
    chunked = False

    for line in header:
        line = line.split(":", 1)
        if (line[0] == "Set-Cookie"):
            cookie_split = line[1].split(";", 1)
            if "csrf" in cookie_split[0]:
                csrf = cookie_split[0]
                if (cookies == ""):
                    cookies = cookies + cookie_split[0]
                else:
                    cookies = cookies + ";" + cookie_split[0]
            else:
                if (cookies == ""):
                    cookies = cookies + cookie_split[0]
                else:
                    cookies = cookies + ";" + cookie_split[0]
        elif (line[0] == "Location"):
            url = line[1].lstrip()
        elif (line[0] == "Content-Length"):
            length = int(line[1])
        elif (line[0] == "Transfer-Encoding"):
            if "chunked" in line[1]:
                chunked = True
        
    parsed_header = {'status':status_num, 'url':url, 'cookie':cookies, 'csrf':csrf, 'chunked':chunked, 'length':length}
    return parsed_header 



# given a request url (String), return a composed one-time
# request message (String) without cookie or token
def http_get(file_path, host_name):
    request = "GET /" + file_path + " HTTP/1.1\r\n"\
              "HOST: " + host_name + "\r\n\r\n"
             #"Cookie:" + cookie + "\r\n\r\n"
             # "X-CSRFTOKEN:" + csrf + "\r\n\r\n"
    return request

