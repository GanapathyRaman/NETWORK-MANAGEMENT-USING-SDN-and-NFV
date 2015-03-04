#!/usr/bin/env python

__author__ = "Ganapathy Raman"

"""
This program acts as a proxy server. On gettting HTTP request, holds the received HTTP request.
It now gets the required parameter from the URL and send the values to the SQL database through simple 
TCP client server communication. It forwards the recived result back to client via HTTP
"""
from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import sqlite3
from os import curdir, sep
import SocketServer
import sys, string,cStringIO, cgi,time,datetime
import socket


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        root = os.path.dirname(__file__)
        self._set_headers()
        query = urlparse(self.path).query
        print query
        if query:
            query_components = dict(qc.split("=") for qc in query.split("&"))
            name = query_components["name"]
            host = '150.0.0.1'
            port = 50000
            size = 1024
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
            s.send(name)
            data = s.recv(size)
            s.close()

            try:
                with open(os.path.join(root, 'result.html')) as f:
                    self.wfile.write(f.read())
            except IOError as e:
                self.write("404: Not Found")

            if data:
                value = []
                for results in data.split():
                    value.append(results)
                self.wfile.write("<tr><td>")
                self.wfile.write(value[1])
                self.wfile.write("</td><td>")
                self.wfile.write(value[2])
                self.wfile.write("</td><td>")
                self.wfile.write(value[3])
                self.wfile.write("</td><td>")
                self.wfile.write(value[4])
                self.wfile.write("</td></tr>")

            try:
                with open(os.path.join(root, 'end.html')) as f:
                    self.wfile.write(f.read())
            except IOError as e:
                self.wfile.write("404: Not Found")

            print "Operation done successfully";
        else:
            try:
                with open(os.path.join(root, 'index.html')) as f:
                    self.wfile.write(f.read())
            except IOError as e:
                self.wfile.write("404: Not Found")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
