"""B данном файе будем обобщать вид входных данных, которые мы получаем"""
from Server.request_processing import *
from Server.exceptions import *
import json
from functools import lru_cache
from urllib.parse import parse_qs, urlparse

"""наш запрос будет выглядеть следующим образом
{"type"(Init,Sys,Trigger,Connect): {
    "device" : "...",
    "data" : "..."
}}
пока так
"""
"""
У нас есть проблема связанная с изменнением ip в сети
если у нас до инициализации человек связывается с не известным
нам ip нужно выбрасывать исключения, для корректной работы
"""

"""
По поводу инициализации: необходимо сначала проинициализировать два независимых 
устройства, а уже потом создавать(инициализировать) пару(которую мы уже продумали)
"""
class Response:
    def __init__(self, status, reason, headers = None, body = None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class Request:
    def __init__(self, method, uri, version, headers, rfile, ip):
        self.method = method
        self.uri = uri
        self.version = version
        self.headers = headers
        self.ip = ip
        self.rfile = rfile

    
    @property
    def path(self):
        return self.url.path
    
    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)
    
    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.uri)

class Raw_request:
    def __init__(self, raw_message, device_ip):
        self.req_dict = json.loads(raw_message)
        self.device_ip = device_ip

    # сразу определяет по типу запроса что мы хотим вообще 
    def generate_type_raw(self):
        try:
            if len(list(self.req_dict.keys())) == 1:
                type_request = list(self.req_dict.keys())
                data = self.req_dict[type_request[0]]
                message = Request_message(type_request[0], data['device'], data['data'], self.device_ip)
                return message
            else:
                raise DefinitionTypeError
        except DefinitionTypeError as e:
            print(e.args[0])


class Request_message:
    def __init__(self, type, device, data, device_ip):
        self.type = type
        self.device = device
        self.device_ip = device_ip
        self.data = data