class ExceptionDetail:

    def __init__(self):
        self._status = None
        self._code = None
        self._error_message = None
        self._user_message = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def error_message(self):
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        self._error_message = error_message

    @property
    def user_message(self):
        return self._user_message

    @user_message.setter
    def user_message(self, user_message):
        self._user_message = user_message

    def __str__(self):
        e_detail = "[ Status: {} || Code : {} || ErrorMessage : {} || UserMessage: {}".format(self.status, self.code,
                                                                                              self.error_message,
                                                                                              self.user_message)

        return e_detail
