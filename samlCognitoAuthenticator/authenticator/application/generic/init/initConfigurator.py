import logging
from application.generic.base.exception.genericExceptions import ApplicationException


class InitConfigurator:

    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    def initialize(self):
        flag = True

        self.logger.debug("InitConfigurator loading the application prerequisites...")

        '''
        try:
            
            # For now, load nothing
        except ApplicationException as aEx:
            self.logger.error("ApplicationException occurred during initializing the application : {}".format(aEx.message))
            flag = False
        except Exception as ex:
            self.logger.error("Exception occurred during initializing the application : {}".format(ex))
            flag = False
        '''

        return flag

