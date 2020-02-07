import logging

from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

from application.authenticate.integration.cognito.facade.userManagement import CognitoUserMgmt
from application.generic.base.exception.exceptionUtility import ExceptionUtility
from application.generic.base.constants.genericConstants import *
from application.generic.base.constants.exceptionConstants import *
from application.generic.base.exception.genericExceptions import *
from application.generic.base.exception.businessExceptions import *


class CognitoAuthBackend():
    logger = logging.getLogger(__name__)

    def authenticate(self, request, **kwargs):
        user = None

        try:
            self.logger.debug("It seems that SAML Based Authentication failed, checking with Email Password "
                              "based authentication")
            self.logger.debug("Inside Email Password Auth Backend - Authenticate ")

            if 'username' in kwargs:
                username = kwargs['username']
                password = kwargs['password']

                # Authenticate in Cognito Pool
                cognitoAuth = CognitoUserMgmt()
                is_user_authenticated = cognitoAuth.cog_authenticate_user(username, password)

                if not is_user_authenticated:
                    raise forms.ValidationError(
                        _("Username / Password Authentication Failed")
                    )

                user = User.objects.get(username=username)
            else:
                self.logger.debug("Username not found in email/password backend.")

        except CognitoUserMgmtException as cogEx:
            self.logger.error("CognitoUserMgmtException occurred in EmailPasswordAuth Custom Backend while "
                              "authenticating user : {}".format(cogEx.message))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           cogEx.message,
                                                           CognitoUserMgmtException.__name__)
        except User.DoesNotExist as dnEx:
            self.logger.error("DoesNotExist occurred in EmailPasswordAuth CustomBackend while authenticating user : {}".
                              format(dnEx))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_BUSINESS_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_BUSINESS_EXCEPTION,
                                                           str(dnEx),
                                                           ApplicationException.__name__)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Djano Admin treats None user as anonymous your who have no right at all.
            return None