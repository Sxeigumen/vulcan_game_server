"""Собственные исключения, для красоты сервера"""
class DefenitionTypeError(Exception):
    def __init__(self):
        self.type_error = "400(Bad Request)"


class LocalBdOverflow(Exception):
    def __init__(self):
        self.type_error = "501(Bd Overflow)"