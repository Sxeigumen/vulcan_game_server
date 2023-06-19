"""Собственные исключения, для красоты сервера"""
class DefinitionTypeError(Exception):
    def __init__(self):
        self.type_error = "400(Bad Request)"


class LocalBdOverflow(Exception):
    def __init__(self):
        self.type_error = "501(Bd Overflow)"


class NotInitSmartphone(Exception):
    def __init__(self):
        self.type_error = "401(Not Init)"