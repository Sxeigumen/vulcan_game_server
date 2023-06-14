import socket
import json
from typing import Any
from data import *
from request_processing import *


def main():
    server = Server('127.0.0.1', 3000)
    server.start_server()



class Data:
    def __init__(self, raw_string):
        self.__dict__ = json.loads(raw_string)


class Server:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(1)

    def start_server(self):
        while True:
            new_socket, from_addr = self.server.accept()
            print(f'Client connected\n\tIP: {from_addr[0]} Port: {from_addr[1]}')
            string = ' '
            string = new_socket.recv(1024)
            raw_data = Raw_request(string, from_addr[0])
            data = raw_data.generate_type_raw()
            request_handler(data)


if __name__ == "__main__":
    main()
