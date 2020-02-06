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

        return (port, host)

    def connect(self, host, port):
        print("In conenct")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return self.socket

    def get_code(self, data):
        print("In code")
        return None

    def get_headers(self,data):
        print("IN HEADER")
        return None

    def get_body(self, data):
        print("In body")
        return None
    
    def sendall(self, data):
        print("in send all")
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

    def GET(self, url, args=None):
        code = 500
        body = ""



        # print(url)
        (port, host) = self.get_host_port(url)
        # print(host)
        remote_ip = socket.gethostbyname(host)
        # print(remote_ip)
        payload = 'GET / HTTP/1.0\r\nHost: ' + host + '\r\n\r\n'
        # print(port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.sendall(payload.encode())
        self.socket.shutdown(socket.SHUT_WR)

        body = self.recvall(self.socket)
        # print(body.split('\n'))
        code = [x for  x in body.split('\n') if "HTTP/1.1" in x][0].split(" ")[1]
        print(code)
        # x = self.connect(remote_ip,  int(host_port[0]))

        # get_command = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host_port[1])
        # print(get_command)

        # self.sendall(get_command)
        # self.close()

        # y = self.recvall(x)

        # print(y)
        # print(x)

        # print(args)
        # print("body: {}".format(body))
        # print("HAD A GET REQUEST")
        #Need to decide code based on url
        # print("HAD A GET REQUEST")
        #Need to call all functions above manually
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        return HTTPResponse(code, body)

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
