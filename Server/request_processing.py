import server
from devices import *
import random
import re
import os
import subprocess
from exceptions import *
import data

max_count_of_string = 10000

def generate_id(device, device_ip):
    gen_id = random.randint(1000,9999)   
    flag = False 
    count_of_string = sum(1 for line in open('localbd.txt', 'r'))
    if count_of_string > max_count_of_string:
        raise LocalBdOverflow
    with open('localbd.txt', 'a+') as file:
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
            file.write(f'{device}:{gen_id}:{device_ip}:{False}\n')
            flag = True
    return gen_id
        
def get_all_controller(name_of_controller = 'all'):
    all_controller = list()
    with open('localbd.txt', 'r') as file:
        while True:
            temp_string = file.readline()
            if temp_string:
                temp_list = temp_string.split(':')
                if temp_list[0] == 'Controller' and temp_list[-1].rstrip('\n') == "False":
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
                #print((temp_list[2])[2:temp_list[2].rfind("'")])
                #print(type(data.ip))
                if data.ip[0] == (temp_list[2])[2:temp_list[2].rfind("'")]:
                    return True
            else:
                break
    return False

"""Идея по поводу генерирования id, пусть они генерируются как для контроллера, так и для телефона(4 цифры к примеру)
а потом уже при подключении просто объединяем их айдишникик и все, получаем айди соединения"""
#более сложный процесс необходимо кроме просто создания также отправлять информацию, что все прошло усепшно
def init_handler(socket, request):
    device = request.headers.get('Device')
    device_ip = request.ip
    if device == 'Controller':
        device_id = generate_id(device, device_ip)
        new_controller = Controller(device_id, device_ip)
        response = data.Response("201", 'Created')
        return response
    elif device == 'Smartphone':
        device_id = generate_id(device, device_ip)
        new_smartphone = Smartphone(device_id, device_ip)
        body = str.encode(''.join(get_all_controller()), 'iso-8859-1')
        print(get_all_controller())
        print(body)
        headers = [('Content-Length', len(body))]
        response = data.Response("200", 'OK', headers, body)
        return response
"""после инициализации необходимо выдавать список всех зарегистрированных контроллеров"""

"""надо перезаписывать"""
def init_pair(data_smartphone, data_controller):
    smartphone_id = ''
    controller_id = ''
    with open('localbd.txt', 'r') as file_read, open('localbd.tmp', 'w') as file_write:
        while True:
            temp_string = file_read.readline()
            if temp_string:
                if data_controller == temp_string:
                    temp_string.replace('False', 'True')
                    file_write.write(temp_string)
                    temp_list = data_controller.split(':')
                    controller_id = temp_list[1]
                    continue
                elif (data_smartphone.headers.get('Device') == temp_list[0] 
                        and data_smartphone.ip[0] == (temp_list[2])[2:temp_list[2].rfind("'")]
                        and temp_list[-1].rstrip('\n') == 'False'):
                    temp_list = temp_string.split(':')
                    temp_string.replace('False', 'True')
                    file_write.write(temp_string)
                    smartphone_id = temp_list[1]
                else:
                    file_write.write(temp_string)
            else:
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'localbd.txt')
                os.remove(path)
                os.rename('localbd.tmp', 'localbd.txt')
                break
    new_pair = DeviceConnection(smartphone_id+controller_id, smartphone_id, controller_id)
    return new_pair

"""пока не знаю как реализовать подключение, точно понимаю, что это sys запрос но пока 
не до конца понимание"""
def system_handler(socket, data):
    pass


"""Пишу что это такое - это то самое, про что мы говорили, это подключение, то есть
генерирование пары, именно подключение с выбранным id controller, также я подумал, что можно сделать важную вещь
например если сначала подключается смартфон, тогда он не выведит ничего полезного(то есть к чему можно подключиться)
если подает запрос с параметром all, ему выведутся все доступные контроллеры"""
def connect_handler(socket, request, id = 'all'):
    device = request.headers.get('Device')
    try:
        if not check_init_smartphone(request):
            raise NotInitSmartphone
        if device == 'Smartphone':
            if id == 'all':
                body = str.encode(''.join(get_all_controller()), 'iso-8859-1')
                headers = [('Content-Length', len(body))]
                response = data.Response(200, 'OK', headers, body)
                return response
            else:
                connection = get_all_controller(id)
                pair = init_pair(request, connection[0])
                print(1)
                body = str.encode(''.join(pair.id), 'iso-8859-1')
                headers = [('Content-Length', len(body))]
                response = data.Response(201, 'Created', headers, body)
                return response
        else:
            raise DefinitionTypeError
    except DefinitionTypeError as e:
        print(e.args[0])
    except NotInitSmartphone as e:
        print(e.args[0])


def trigger_handler(socket, data):
    """I don't know"""
