import socket
from email import parser
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from sql import Database
from data import Request, Response
from request_processing import init_handler, connect_handler
import logg

MAX_LINE = 64*1024
MAX_HEADER = 100
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'postres')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_NAME = os.environ.get('DB_NAME', 'connection')
DB_PASS = os.environ.get('DB_PASS', 'Kyala')

def main():
    server = Server('192.168.220.3', 8080, 'proxi')
    server.create_connection_database(DB_USER, DB_PASS, DB_NAME)
    server.server_forever()


class Server:
    def __init__(self, ip, port, server_name):
        self.ip = ip
        self.port = port
        self.server_name = server_name
    
    def create_connection_database(self, user, password, db_name):
        self.database = Database('192.168.220.4', user, password, db_name)

    def server_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        try:
            server_socket.bind((self.ip, self.port))
            server_socket.listen()

            while True:
                new_socket, from_addr = server_socket.accept()
                self.socket = new_socket
                try:
                    print(from_addr)
                    self.server_client(new_socket)
                    logg.server_logger.info(f'Successful connection: {from_addr}')
                except Exception as e:
                    print('Client serving failed', e)
                    logg.server_logger.exception(f'Client serving failed {from_addr}')
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
        headers = self.parse_request_header(rfile)
        host = headers.get('Host')
        if version != 'HTTP/1.1':
            raise Exception(f'Unexpected HTTP version - {headers}')
        if not host:
            raise Exception('Bad request')
        if host not in (self.server_name, f'{self.ip}:{self.port}'):
            raise Exception(f'Not right connection - exected {self.ip}:{self.port} not {host}')
        return Request(method, uri, version, headers, rfile, headers.get('X-Forwarded-For'))

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
        return parser.Parser().parsestr(headers_dict)
    
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
    INIT /device - инициализация устроства
    POST /trigger - отправка данных при триггере"""

    def handle_request(self, request):
        if request.path == '/controller' and request.method == 'GET':
            return self.handle_get_controllers(request)
        if request.path == '/device' and request.method == 'INIT':
            return self.handle_init_device(request)
        if '/controller/' in request.path and request.method == 'GET':
            controller_id = request.path[len('/controller/'):]
            if controller_id.isdigit():
                return self.handle_get_controller(request, controller_id)

    def handle_get_controllers(self, request):
        return connect_handler(self.socket, request, self.database)
    
    def handle_get_controller(self, request, id):
        return connect_handler(self.socket, request, self.database, id)

    def handle_init_device(self, request):
        return init_handler(self.socket, request, self.database)

    def send_response(self, socket, response):
        wfile = socket.makefile('wb')
        status_line = f'HTTP/1.0 {response.status} {response.reason}\r\n'
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
    #Необходимо нормально проделать обработчик ошибок, пока это просто 400
    def send_error(self, socket, error):
        response = Response('400', f'{error}')
        self.send_response(socket, response)
           


if __name__ == "__main__":
    main()
