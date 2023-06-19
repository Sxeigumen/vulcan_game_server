import server
from Server.data import *
from devices import *
import random
import re
from exceptions import *

init_request = "Init"
system_request = "Sys"
trigger_request = "Trigger"
connect_request = "Connect"
max_count_of_string = 10000


def request_handler(socket, data):
    request_type = data.type

    if  request_type == init_request:
        init_handler(socket, data)
        return
    
    elif request_type == system_request:
        system_handler(socket, data)
        return
    
    elif request_type == trigger_request:
        trigger_handler(socket, data)
        return
    
    elif request_type == connect_request:
        connect_handler(socket, data)
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
            else:
                break
        if not flag:
            file.write(f'{device}:{gen_id}:{device_ip}:{False}')
            flag = True
    return gen_id
        
def get_all_controller(name_of_controller = 'all'):
    all_controller = list()
    with open('localbd.txt', 'r') as file:
        while True:
            temp_string = file.readline()
            if temp_string:
                temp_list = temp_string.split(':')
                if temp_list[0] == 'Controller' and bool(temp_list[-1]):
                    if name_of_controller == 'all':
                        all_controller.append(temp_string)
                    else:
                        all_controller.append(temp_string)
                        break
            else:
                break
    return all_controller

def check_init_smartphone(data):
    with open('localbd.txt', 'r') as file:
        while True:
            temp_string = file.readline()
            if temp_string:
                temp_list = temp_string.split(':')
                if data.device_ip == temp_list[2]:
                    return True
            else:
                break
    return False

"""Идея по поводу генерирования id, пусть они генерируются как для контроллера, так и для телефона(4 цифры к примеру)
а потом уже при подключении просто объединяем их айдишникик и все, получаем айди соединения"""
#более сложный процесс необходимо кроме просто создания также отправлять информацию, что все прошло усепшно
def init_handler(socket, data):
    device = data.device
    if device == 'Controller':
        device_id = generate_id(device, data.device_ip)
        new_controller = Controller(device_id, data.device_ip)
        socket.sendall(b'OK')

    elif device == 'Smartphone':
        device_id = generate_id(device, data.device_ip)
        new_smartphone = Smartphone(device_id, data.device_ip)
        socket.sendall(b';'.join(get_all_controller()))
        """после инициализации необходимо выдавать список всех зарегистрированных контроллеров"""

def init_pair(data_smartphone, data_controller):
    smartphone_id = ''
    controller_id = ''
    with open('localbd.txt', 'r') as file:
        while True:
            temp_string = file.readline()
            if temp_string:
                if data_controller == temp_string:
                    temp_string.replace('Flase', 'True')
                    temp_list = data_controller.split(':')
                    controller_id = temp_list[1]
                    continue
                temp_list = temp_string.split(':')
                if data_smartphone.device == temp_list[0] and data_smartphone.device_ip == temp_list[2] and bool(temp_list[-1]):
                    temp_string.replace('False', 'True')
                    smartphone_id = temp_list[1]
            else:
                break
    new_pair = DeviceConnection(smartphone_id+controller_id, smartphone_id, controller_id)

"""пока не знаю как реализовать подключение, точно понимаю, что это sys запрос но пока 
не до конца понимание"""
def system_handler(socket, data):
    pass


"""Пишу что это такое - это то самое, про что мы говорили, это подключение, то есть
генерирование пары, именно подключение с выбранным id controller, также я подумал, что можно сделать важную вещь
например если сначала подключается смартфон, тогда он не выведит ничего полезного(то есть к чему можно подключиться)
если подает запрос с параметром all, ему выведутся все доступные контроллеры"""
def connect_handler(socket, data):
    device = data.device
    try:
        if not check_init_smartphone(data):
            raise NotInitSmartphone
        if device == 'Smartphone':
            id_to_connect = data.data
            if id_to_connect == 'all':
                all_available_connections = get_all_controller()
                socket.sendall(b';'.join(get_all_controller()))
            else:
                connection = get_all_controller(id_to_connect)
                init_pair(data, connection)
                socket.sendall(b'OK')
        else:
            raise DefinitionTypeError
    except DefinitionTypeError as e:
        print(e.args[0])
    except NotInitSmartphone as e:
        print(e.args[0])


def trigger_handler(socket, data):
    """I don't know"""
