#!/usr/bin/python3

import pycparser
import http.server
import socketserver
from pathlib import Path

import parse

PORT = 8000

def startServer(path):
    print('Launching server. ')
    jsCode = parse.getJsFuncDefs(path)
    handler = RequestHandler
    handler.jsFuncDefs = jsCode;
    httpd = socketserver.TCPServer(("", 8000), handler)
    httpd.serve_forever()

class RequestHandler(http.server.BaseHTTPRequestHandler):

    jsFuncDefs = ''

    def do_GET(self):
        if (self.path == '/three.js'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            with Path('three.js').open(mode='rb') as f:
                self.wfile.write(f.read())
        elif (self.path == '/'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            with Path('template.html').open(mode='rb') as f:
                self.wfile.write(f.read().replace(b'//FUNCDEFS', self.jsFuncDefs.encode()))
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(b'not found')



