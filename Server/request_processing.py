import server

init_request = "Init"
system_request = "Sys"
trigger_request = "Trigger"


def request_handler(data):
    request_type = data.type

    if request_type == init_request:
        init_handler(data)
        return
    elif request_type == system_request:
        system_handler(data)
        return
    elif trigger_handler == trigger_request:
        init_handler(data)
        return


def init_handler(data):
    """Что-то будет"""


def system_handler(data):
    """Продолжение следует..."""


def trigger_handler(data):
    """I don't know"""


def id_generator():
    """Надо думать"""

