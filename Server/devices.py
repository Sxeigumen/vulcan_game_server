
class Controller:
    def __init__(self, device_id, device_ip):
        self.id = device_id
        self.ip = device_ip
        self.connection_with_smartphone = False
        "Можно добавить ещё полей, но пока пусть будет так"


class Smartphone:
    def __init__(self, device_id, device_ip):
        self.id = device_id
        self.ip = device_ip
        "Можно добавить ещё полей, но пока пусть будет так"


class DeviceConnection:
    def __init__(self, pair_id, controller, smartphone):
        self.id = pair_id
        self.controller_ip = controller.ip
        self.smartphone_ip = smartphone.ip

    """Надо будет подумать как генерить id, чтобы корректно работать. Типо чтоб они могли удаляться и создаваться без
        каких-то проблем. Это будем делать видимо в функции init_handler которая лежит в другом файле"""