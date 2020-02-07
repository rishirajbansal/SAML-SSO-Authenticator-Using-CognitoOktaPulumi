import logging
from .businessExceptions import *
from .serviceExceptions import *
from .genericExceptions import *


class ExceptionUtility:
    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    @staticmethod
    def create_exception_detail(error_code, user_message, error_message, exception_type):
        app_exception = None

        exception_detail = ExceptionDetail()
        exception_detail.code = error_code
        exception_detail.error_message = error_message
        exception_detail.user_message = user_message

        if exception_type == ApplicationException.__name__ :
            app_exception = ApplicationException()
        elif exception_type == InitException.__name__ :
            app_exception = InitException()
        elif exception_type == BusinessException.__name__:
            app_exception = BusinessException()
        elif exception_type == BusinessValidationException.__name__:
            app_exception = BusinessValidationException()
        elif exception_type == DataAccessException.__name__:
            app_exception = DataAccessException()
        elif exception_type == CognitoUserMgmtException.__name__:
            app_exception = CognitoUserMgmtException()
        elif exception_type == AuthAPIManagementException.__name__:
            app_exception = AuthAPIManagementException()
        else:
            ExceptionUtility.logger.error("Invalid exception type")

        if app_exception is not None:
            app_exception.set_exception_detail(exception_detail)

        return app_exception

    @staticmethod
    def create_exception_detail_by_obj(exception_detail, exception_type):
        return ExceptionUtility.create_exception_detail(exception_detail.code, exception_detail.error_message,
                                                        exception_detail.user_message, exception_type)
