from devices import *
from exceptions import *
import data

max_count_of_string = 10000
        
def get_string_from_controllers(db, id = 'all'):
    list_tuples = get_all_controller(db, id)
    string_to_translate = ''
    for tup in list_tuples:
        tup = str(tup)
        string_to_translate += tup + '; '
    return string_to_translate

def get_all_controller(database, id_controller = 'all'):
    try:
        all_controller = list()
        if id_controller == 'all':
            all_controller = database.Select_one('Controllers', 'connection', False)
        else:
            all_controller = database.Select_one('Controllers', 'id', id_controller)
            if all_controller[2]:
                raise Exception
        return all_controller
    except Exception as er:
        raise ConnectAlreadyHave

def check_init_smartphone(data, database):
    device_ip = data.ip
    smartphone  = database.Select_one('Smartphones', 'ip', device_ip)
    if not smartphone:
        return False
    else:
        return True

"""Идея по поводу генерирования id, пусть они генерируются как для контроллера, так и для телефона(4 цифры к примеру)
а потом уже при подключении просто объединяем их айдишникик и все, получаем айди соединения"""
#более сложный процесс необходимо кроме просто создания также отправлять информацию, что все прошло усепшно
def init_handler(socket, request, database):
    device = request.headers.get('Device')
    device_ip = request.ip
    if device == 'Controller':
        database.Insert('Controllers', 'ip', 'connection', device_ip, False)
        device_id = database.Select_one('Controllers', 'ip', device_ip, 'id')
        new_controller = Controller(device_id, device_ip)
        response = data.Response("201", 'Created')
        return response
    elif device == 'Smartphone':
        database.Insert('Smartphones', 'ip', 'connection', device_ip, False)
        device_id = database.Select_one('Smartphones', 'ip', device_ip, 'id')
        new_smartphone = Smartphone(device_id, device_ip)
        body = str.encode(get_string_from_controllers(database), 'iso-8859-1')
        headers = [('Content-Length', len(body))]
        response = data.Response("200", 'OK', headers, body)
        return response

"""надо перезаписывать"""
def init_pair(data_smartphone, data_controller, database):
    smartphone_ip = data_smartphone.ip
    smartphone_id = database.Select_one('Smartphones', 'ip', smartphone_ip)[0]
    controller_id = data_controller[0]
    database.Update('Smartphones', 'connection', True, 'id', smartphone_id)
    database.Update('Controllers', 'connection', True, 'id', controller_id)
    database.Insert('Pairs', 'id_controller', 'id_smartphone', controller_id, smartphone_id)
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
def connect_handler(socket, request, database, id = 'all'):
    device = request.headers.get('Device')
    try:
        if not check_init_smartphone(request, database):
            raise NotInitSmartphone
        if device == 'Smartphone':
            if id == 'all':
                body = str.encode(get_string_from_controllers(database), 'iso-8859-1')
                headers = [('Content-Length', len(body))]
                response = data.Response(200, 'OK', headers, body)
                return response
            else:
                connection = get_all_controller(database, id)
                pair = init_pair(request, connection, database)
                body = str.encode(get_string_from_controllers(database, pair.controller_id), 'iso-8859-1')
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
