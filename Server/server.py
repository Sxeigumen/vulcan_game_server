import socket
import email
import json
from typing import Any
from data import *
from request_processing import *
from functools import lru_cache
from urllib.parse import parse_qs, urlparse

MAX_LINE = 64*1024
MAX_HEADER = 100

def main():
    server = Server('127.0.0.1', 80, 'proxi')
    server.server_forever()

"""Для начала хочу здесь реализовать API вида инициализации и создания пары"""

class Server:
    def __init__(self, ip, port, server_name):
        self.ip = ip
        self.port = port
        self.server_name = server_name

    def server_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            server_socket.bind((self.ip, self.port))
            server_socket.listen()

            while True:
                new_socket, from_addr = server_socket.accept()
                self.socket = new_socket
                self.ip_connect = from_addr
                try:
                    self.server_client(new_socket)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            server_socket.close()

    def server_client(self, socket):
        try:
           request = self.parse_request(socket)
           response = self.handle_request(request)
           self.send_response(socket, response)
        except ConnectionResetError:
           socket = None
        except Exception as e:
           self.send_error(socket, e)
        if socket:
            socket.close()

    def parse_request(self, socket:socket.socket):
        rfile = socket.makefile('rb')
        method, uri, version = self.parse_request_line(rfile)
        if version != 'HTTP/1.1':
            raise Exception('Unexpected HTTP version')
        headers = self.parse_request_header(rfile)
        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')
        if host not in (self.server_name, f'{self.ip}:{self.port}'):
            raise Exception('Not right connection')
        return Request(method, uri, version, headers, rfile, self.ip_connect)

    def parse_request_header(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise Exception('Header line is too long')
            if line in (b'\r\n', b'\n', b''):
                break
            headers.append(line)
            if len(headers) > MAX_HEADER:
                raise Exception('Too mane headers')
        headers_dict = b''.join(headers).decode('iso-8859-1')
        return email.Parser().parsestr(headers_dict)
    
    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise Exception('Request line is too long')
        request_line = str(raw, 'iso-8859-1')
        request_line = request_line.rstrip('\r\n')
        words = request_line.split(' ')
        if len(words) != 3:
            raise Exception('Incorrect request line')
        return words


    """GET /controller - получение всех инициализированных контроллеров
    POST /controller/id - подключение смартфона к определенному контроллеру
    INIT /device - инициализация устроства"""

    def handle_request(self, request):
        if request.path == '/controller' and request.method == 'GET':
            return self.handle_get_controllers(request)
        if request.path == '/device' and request.method == 'INIT':
            return self.handle_init_device(request)
        if request.path.startwith('/controller/') and request.method == 'GET':
            controller_id = request.path[len('/controller/'):]
            if controller_id.isdigit():
                return self.handle_get_controller(request, controller_id)
        
    
    def handle_get_controllers(self, request):
        return connect_handler(self.socket, request)
    
    def handle_get_controller(self, request, id):
        return connect_handler(self.socket, request, id)

    def handle_init_device(self, request):
        return init_handler(self.socket, request)

    def send_response(self, socket, response):
        wfile = socket.makefile('wb')
        status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))
        if response.headers:
            for (key, value) in response.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))
        wfile.write(b'\r\n')
        if response.body:
            wfile.write(response.body)
        wfile.flush()
        wfile.close()

    def send_error(self, socket, error):
        response = Response('400', f'{error}')
        self.send_response(socket, response)
           


if __name__ == "__main__":
    main()
