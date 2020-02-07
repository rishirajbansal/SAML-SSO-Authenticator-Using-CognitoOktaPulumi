from application.generic.base.exception.exceptionDetail import *


class ApplicationException(Exception):
    exception_detail = ExceptionDetail()
    message = ''

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message

    def get_exception_detail(self):
        return self.exception_detail

    def set_exception_detail(self, exception_detail):
        self.exception_detail = exception_detail
        self.message = exception_detail.error_message

