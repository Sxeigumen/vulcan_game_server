import socket
import json
from typing import Any

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
            data = Data(string)
            print(data.name)
            print(data.surname)

if __name__ == "__main__":
    main()
