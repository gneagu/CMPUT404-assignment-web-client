#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        # self.socket = socket
        self.code = code
        self.body = body

class HTTPClient(object):
    #Refer to https://uofa-cmput404.github.io/cmput404-slides/05-More-HTTP.html#/8
    #Essentilly, keep up to either first formward slash (after http://, or till end)
    def get_host_port(self,url):
        port = ""
        removed_http = url.replace("http://", "",1)
        host = removed_http.split('/')[0]

        pre_host = host.split(':')
        if len(pre_host) != 1:
            port = pre_host[1]
        else:
            port = 80
        new_host = self.decide_if_localhost(host)

        return (int(port), new_host, host)

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return self.socket

    def get_code(self, data):
        code_string = [x for  x in data.split('\n') if "HTTP/1." in x]
        code = int(code_string[0].split(" ")[1])
        return(code)
        
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        print(data.encode('utf-8'))
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.shutdown(socket.SHUT_WR)
 
    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')
    
    def decide_if_localhost(self, host):
        host_return = ""
        if "127.0.0.1" in host:
            host_return = "localhost"
        else:
            host_return = host
        return(host_return)

    def GET(self, url, args=None):
        code = 500
        body = ""

        (port, host) = self.get_host_port(url)
        payload = 'GET / HTTP/1.0\r\nHost: ' + host + '\r\n\r\n'

        self.connect(host, int(port))
        self.sendall(payload)
        self.close()

        body = self.recvall(self.socket)
        code = self.get_code(body)

        return HTTPResponse(code, body)

    def POST(self, url, args):
        code = 500
        body = ""

        # string_args = string_args + x for x in args
        # print(string_args) 
        
        # print(args)
        string_args = "{\n"

        for x, y in args.items():
            # print("LOOPS", x)
            string_args += '''  "{}" : '{}',\n'''.format(x,y)


        string_args = string_args + "}"



        # print("URL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(url)
        # print(args)
        # print(type(args))

        # print("END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # x = '{\n"Id": 12345,\n"Customer": "John Smith",\n"Quantity": 1,\n"Price": 10.00\n}'
        # print("XXXXXXXXXXXXXXXXXXXXXXX")
        # print(x)
        (port, new_host, host) = self.get_host_port(url)
        # payload = 'POST / HTTP/1.0\r\nHost: ' + host + '\r\n\Content-type: text/html\r\nContent-length: 0\r\n\r\n'

        payload = 'POST /session HTTP/1.0\r\n\
Host: ' + host + '''\r\n\
Content-type: application/json\r\n\
Content-length: %s\
\r\n\r\n\
{"a": "aaaaaaaaaaaaa", "b": "bbbbbbbbbbbbbbbbbbbbbb", "c": "c", "d": "012345\r67890\n2321321\n\r"}''' % (len(str(string_args)))

        # print("URL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # print(payload)
        # # print(len(x), x)
        # print("END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


        #NEED TO MAKE SURE THAT newline and carriage return have double \\ otherwise seen as control characters
        # https://stackoverflow.com/questions/45695168/send-raw-post-request-using-socket
        derp = '''{"a": "aaaaaaaaaaaaa", "b": "bbbbbbbbbbbbbbbbbbbbbb", "c": "c", "d": "012345\\r67890\\n2321321\\n\\r"}'''

        self.connect(new_host, int(port))
        self.sendall(payload)
        self.close()
        print("Before body")
        body = self.recvall(self.socket)
        print("After bpdy``````````````````````````````")
        print(body)
        code = self.get_code(body)
        # print(code)

        return HTTPResponse(code, derp)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
