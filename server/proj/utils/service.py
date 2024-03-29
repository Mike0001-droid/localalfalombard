from abc import ABC
from utils.transport import REST, TransportError, AccessBlockError

class ServiceError(TransportError):
    pass

class SettingsSiteError(AccessBlockError):
    pass


class Service(ABC):
    transport = None

    def call(self, method, *args, **kwargs):
        return self.transport.call(method, *args, **kwargs)


class RESTService(Service):
    transport = REST()

    def call(self, method, *args, **kwargs):
        try:
            return self.transport.call(method, *args, **kwargs)
        
        except TransportError as e:
            raise ServiceError(str(e), e.code)
        
        except AccessBlockError as e:
            raise SettingsSiteError(e.message)
