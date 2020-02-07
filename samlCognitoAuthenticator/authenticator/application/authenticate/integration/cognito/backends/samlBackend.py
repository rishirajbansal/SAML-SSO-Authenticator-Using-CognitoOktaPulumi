import logging
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

from application.authenticate.integration.cognito.facade.authAPIManagement import OAuthManager
from application.authenticate.integration.cognito.facade.userManagement import CognitoUserMgmt
from application.generic.base.exception.exceptionUtility import ExceptionUtility
from application.generic.base.constants.genericConstants import *
from application.generic.base.constants.exceptionConstants import *
from application.generic.base.exception.genericExceptions import *
from application.generic.base.exception.businessExceptions import *


class CognitoAuthBackend:
    logger = logging.getLogger(__name__)

    def authenticate(self, request, **kwargs):
        user = None
        username = None
        authorization_code = None
        id_token = None
        access_token = None
        refresh_token = None
        error = None
        is_token = False

        try:
            self.logger.debug("Inside SAML Auth Backend - Authenticate ")

            if authorization_code in kwargs:

                authorization_code = kwargs['authorization_code']

                # if request is not None:
                #     authorization_code = request.GET.get("code")

                # Check if code exists, then only proceed
                if authorization_code is not None:

                    # Get Auth Tokens
                    oAuthManager = OAuthManager(os.getenv("AWS_COGNITO_CLIENT_ID"),
                                                os.getenv("AWS_COGNITO_CLIENT_SECRET"),
                                                os.getenv("AWS_COGNITO_REDIRECT_URI"),
                                                os.getenv("AWS_COGNITO_DOMAIN"),
                                                os.getenv("AWS_REGION")
                                                )

                    oAuthManager.set_token_endpoint()

                    response_status, data = oAuthManager.post_token_endpoint_request(authorization_code)

                    if response_status == 200:
                        id_token = data["id_token"]
                        access_token = data["access_token"]
                        refresh_token = data["refresh_token"]
                        token_type = data["token_type"]
                        expires_in = data["expires_in"]

                        is_token = True

                    elif response_status == 400:
                        error = data["error"]

                    else:
                        error = "Invalid Status received from OAuth Manager"

                    # Get the User details from Cognito Uesr Pool based on the tokens
                    if is_token:
                        self.logger.debug("AUTHORIZATION GRANT based authentication is successfull and received valid tokens.")
                        self.logger.debug("Getting User data from Cognitio User pool based on the tokens...")

                        cognitoAuth = CognitoUserMgmt()
                        is_user_authenticated, username = cognitoAuth.cog_saml_authenticate_user(id_token,
                                                                                                 refresh_token,
                                                                                                 access_token)

                        if not is_user_authenticated:
                            raise forms.ValidationError(
                                _("SSO Authentication Failed")
                            )

                        user = User.objects.get(username=username)

                    else:
                        self.logger.debug("AUTHORIZATION GRANT based authentication FAILED.")
                        self.logger.debug("ERROR : {0}".format(error))

                        # raise forms.ValidationError(
                        #     _("SSO Error: {0}".format(error))
                        # )
                else:
                    self.logger.debug("Authorization Code not found, authentication process will try another backend.")
            else:
                self.logger.debug("Authorization Code not found, authentication process will try another backend.")

        except CognitoUserMgmtException as cogEx:
            self.logger.error("CognitoUserMgmtException occurred in SAML Custom Backend while "
                              "authenticating user : {}".format(cogEx.message))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                           cogEx.message,
                                                           CognitoUserMgmtException.__name__)
        except User.DoesNotExist as dnEx:
            self.logger.info("DoesNotExist occurred in SAML Custom Backend while authenticating user : {}".
                              format(dnEx))
            self.logger.info("New user will be created for : {}".format(username))

            # Create User as it is coming Form Okta after SAML verification from Cognito

            user = User(username=username, email=username)
            user.is_staff = True
            user.is_superuser = True
            user.save()

            # raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_BUSINESS_EXCEPTION,
            #                                                ExceptionConstants.USERMESSAGE_BUSINESS_EXCEPTION,
            #                                                str(dnEx),
            #                                                ApplicationException.__name__)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Djano Admin treats None user as anonymous your who have no right at all.
            return None