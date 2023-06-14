import server
from Server.data import *
from devices import *
import random

init_request = "Init"
system_request = "Sys"
trigger_request = "Trigger"



def request_handler(data):
    request_type = data.type

    if  request_type== init_request:
        init_handler(data)
        return
    elif request_type == system_request:
        system_handler(data)
        return
    elif request_type == trigger_request:
        init_handler(data)
        return

def generate_id(device):
    pass

"""Идея по поводу генерирования id, пусть они генерируются как для контроллера, так и для телефона(4 цифры к примеру)
а потом уже при подключении просто объединяем их айдишникик и все, получаем айди соединения"""
def init_handler(data):
    device = data.device
    if device == 'Controller':
        device_id = generate_id(device)
        new_controller = Controller(device_id, data.device_ip)

    elif device == 'Smartphone':
        device_id = generate_id(device)
        new_smartphone = Smartphone(device_id, data.device_ip)



def system_handler(data):
    """Продолжение следует..."""


def trigger_handler(data):
    """I don't know"""


def id_generator():
    """Надо думать"""

