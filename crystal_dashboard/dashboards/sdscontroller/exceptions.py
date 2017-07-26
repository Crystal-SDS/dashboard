from horizon import exceptions


class SdsException(exceptions.HorizonException):
    def __init__(self, message):
        super(SdsException, self).__init__(message)