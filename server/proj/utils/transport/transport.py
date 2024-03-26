from abc import ABC


class TransportError(Exception):
    def __init__(self, message, jsn=None, code=99):
        super().__init__(message)
        self.code = code
        self.jsn = jsn

class AccessBlockError(Exception):
    def __init__(self, message):
        self.message = message


class Transport(ABC):
    url = None
    username = None
    password = None
    timeout = None

    def call(self, method, *args, **kwargs):
        raise NotImplementedError('Method should be overridden')
