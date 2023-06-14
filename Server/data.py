"""B данном файе будем обобщать вид входных данных, которые мы получаем"""
from Server.request_processing import *
from Server.exceptions import *
import json

"""наш запрос будет выглядеть следующим образом
{"type"(Init,Sys,Trigger): {
    "device" : "...",
    "data" : "..."
}}
пока так
"""


class Raw_request:
    def __init__(self, raw_message, device_ip):
        self.__dict__ = json.loads(raw_message)
        self.device_ip = device_ip

    # сразу определяет по типу запроса что мы хотим вообще 
    def generate_type_raw(self):
        try:
            if len(list(self.__dict__.keys())) == 1:
                type_request = list(self.__dict__.keys())
                data = self.__dict__[type_request[0]]
                message = Request_message(type_request, data['device'], data['data'], self.device_ip)
                return message
            else:
                raise DefenitionTypeError
        except DefenitionTypeError as e:
            print(e.args[0])


class Request_message:
    def __init__(self, type, device, data, device_ip):
        self.type = type
        self.device = device
        self.device_ip = device_ip
        self.data = data