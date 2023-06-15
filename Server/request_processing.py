import server
from Server.data import *
from devices import *
import random
import re
from exceptions import *

init_request = "Init"
system_request = "Sys"
trigger_request = "Trigger"
max_count_of_string = 10000


def request_handler(data):
    request_type = data.type

    if  request_type == init_request:
        init_handler(data)
        return
    elif request_type == system_request:
        system_handler(data)
        return
    elif request_type == trigger_request:
        init_handler(data)
        return

def generate_id(device, device_ip):
    gen_id = random.randint(1000,9999)   
    flag = False 
    count_of_string = sum(1 for line in open('file', 'r'))
    if count_of_string > max_count_of_string:
        raise LocalBdOverflow
    with open('localbd.txt', 'ra') as file:
        while True:
            temp_string = file.readline()
            if temp_string:
                temp_list = temp_string.split(':')
                if temp_list[0] != device:
                    continue
                else:
                    if int(temp_list[1]) == gen_id:
                        gen_id = generate_id(device, device_ip)
                        break
            break
        if not flag:
            file.write(f'{device}:{gen_id}:{device_ip}')
            flag = True
    return gen_id
        


"""Идея по поводу генерирования id, пусть они генерируются как для контроллера, так и для телефона(4 цифры к примеру)
а потом уже при подключении просто объединяем их айдишникик и все, получаем айди соединения"""
def init_handler(data):
    device = data.device
    if device == 'Controller':
        device_id = generate_id(device, data.device_ip)
        new_controller = Controller(device_id, data.device_ip)

    elif device == 'Smartphone':
        device_id = generate_id(device, data.device_ip)
        new_smartphone = Smartphone(device_id, data.device_ip)



def system_handler(data):
    """Продолжение следует..."""


def trigger_handler(data):
    """I don't know"""
