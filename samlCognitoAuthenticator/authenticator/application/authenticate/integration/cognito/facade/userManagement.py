import logging

from application.authenticate.integration.cognito.facade.facade import CognitoFacade
from application.generic.base.constants.genericConstants import *
from application.generic.base.constants.exceptionConstants import *
from application.generic.base.exception.genericExceptions import *
from application.generic.base.exception.businessExceptions import *
from application.generic.base.exception.exceptionUtility import ExceptionUtility


class CognitoUserMgmt:
    logger = logging.getLogger(__name__)

    def __init__(self):
        cognitoFacade = CognitoFacade()
        self._cognitoFacade = cognitoFacade

    def cog_authenticate_user(self, username, password):
        is_user_authenticated = False

        try:
            self.logger.debug("Authenticating user in Cognito User Pool for email/password...")

            cognito = self._cognitoFacade.get_cognito(username)

            is_user_authenticated = self._cognitoFacade.authenticate(cognito, password)

        except Exception as ex:
            self.logger.error("Exception occurred in Cognito User Management while authenticating user : {}".format(ex))
            # raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
            #                                                ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
            #                                                str(ex),
            #                                                CognitoUserMgmtException.__name__)

        return is_user_authenticated

    def cog_saml_authenticate_user(self, id_token, refresh_token, access_token):
        is_user_authenticated = False
        username = None

        try:
            self.logger.debug("Authenticating user in Cognito User Pool for SAML...")

            cognito = self._cognitoFacade.get_cognito_from_tokens(id_token, refresh_token, access_token)

            user = cognito.get_user(attr_map={"email": "email"})
            data = user._data

            if data["email"] is not None:
                is_user_authenticated = True
                username = data["email"]

        except Exception as ex:
            self.logger.error("Exception occurred in Cognito User Management while SAML authenticating user : {}".
                              format(ex))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           str(ex),
                                                           CognitoUserMgmtException.__name__)

        return is_user_authenticated, username


    def cog_create_user(self, username, email, password):
        try:
            self.logger.debug("Creating user in Cognito User Pool...")

            cognito = self._cognitoFacade.get_cognito(username)

            self._cognitoFacade.create_user(cognito, username, email, password)

        except Exception as ex:
            self.logger.error("Exception occurred in Cognito User Management while creating user in Cognito User Pool "
                              ": {}".format(ex))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           str(ex),
                                                           CognitoUserMgmtException.__name__)

    ####
    # Updating User - Updating user name is not supported as password stored in Django is in hash format
    # Also, once the user is created in Cognito, its username can't be changesd, one way is to delete and then create
    # new user with updated username but for this need a passowrd which is in encrypted form in Django
    ####
    def cog_update_user(self, old_username, new_username, email, password):
        try:
            self.logger.debug("Updating user in Cognito User Pool...")

            cognito = self._cognitoFacade.get_cognito(old_username)

            self._cognitoFacade.update_user(cognito, old_username, new_username, email, password)

        except Exception as ex:
            self.logger.error("Exception occurred in Cognito User Management while updating user in Cognito User Pool "
                              ": {}".format(ex))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           str(ex),
                                                           CognitoUserMgmtException.__name__)

    def cog_delete_user(self, username):
        try:
            self.logger.debug("Deleting user from Cognito User Pool...")

            cognito = self._cognitoFacade.get_cognito(username)

            self._cognitoFacade.delete_user(cognito)

        except Exception as ex:
            self.logger.error("Exception occurred in Cognito User Management while deleting user from Cognito User "
                              "Pool : {}".format(ex))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           str(ex),
                                                           CognitoUserMgmtException.__name__)

    def cog_change_pwd(self, username, old_password, new_password):
        try:
            self.logger.debug("Changing User Password in Cognito User Pool...")

            cognito = self._cognitoFacade.get_cognito(username)

            self._cognitoFacade.change_password(cognito, username, old_password, new_password)

        except Exception as ex:
            self.logger.error("Exception occurred in Cognito User Management while changing password in Cognito User "
                              "Pool : {}".format(ex))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           str(ex),
                                                           CognitoUserMgmtException.__name__)
