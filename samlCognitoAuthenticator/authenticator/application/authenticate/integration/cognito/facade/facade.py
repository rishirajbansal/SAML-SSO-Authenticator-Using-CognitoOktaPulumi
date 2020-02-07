from warrant import Cognito
import logging
import os

from application.generic.base.constants.genericConstants import GenericConstants
from application.generic.utilities.utility import Utility


class CognitoFacade:
    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    def get_cognito(self, username=None):
        cognito = None

        # If required AWS IAM Access key and Secret key can also be passed here. Currently it uses default aws profile
        # Pass these attributes in this constructor for passing non-default AWS Keys
        # access_key=None, secret_key=None
        if Utility.safe_trim(username) != GenericConstants.EMPTY_STRING:
            cognito = Cognito(os.getenv("AWS_COGNITO_USER_POOL_ID"),
                              os.getenv("AWS_COGNITO_CLIENT_ID"),
                              user_pool_region=os.getenv("AWS_REGION"),
                              client_secret=os.getenv("AWS_COGNITO_CLIENT_SECRET"),
                              username=username
                              )
        else:
            cognito = Cognito(os.getenv("AWS_COGNITO_USER_POOL_ID"),
                              os.getenv("AWS_COGNITO_CLIENT_ID"),
                              user_pool_region=os.getenv("AWS_REGION"),
                              client_secret=os.getenv("AWS_COGNITO_CLIENT_SECRET")
                              )

        return cognito

    def get_cognito_from_tokens(self, id_token, refresh_token, access_token):
        cognito = None

        cognito = Cognito(os.getenv("AWS_COGNITO_USER_POOL_ID"),
                          os.getenv("AWS_COGNITO_CLIENT_ID"),
                          user_pool_region=os.getenv("AWS_REGION"),
                          id_token=id_token,
                          refresh_token=refresh_token,
                          access_token=access_token
                          )

        return cognito

    def authenticate(self, cognito, password):
        try:
            cognito.authenticate(password=password)

        except cognito.client.exceptions.NotAuthorizedException as cog_notAuthEx:
            self.logger.error("NotAuthorizedException exception occurred from Cognito - user is not authorized")
            return False

        access_token = cognito.access_token
        id_token = cognito.id_token
        refresh_token = cognito.refresh_token

        user = cognito.get_user(attr_map={"email": "email"})
        user_email = user._data['email']

        if Utility.safe_trim(access_token) != GenericConstants.EMPTY_STRING:
            return True
        else:
            return False

    def create_user(self, cognito, username, email, password):
        cognito.add_base_attributes(email=email)

        cognito.register(username, password)

        cognito.admin_confirm_sign_up(username=username)

    def update_user(self, cognito, old_username, new_username, email, password):
        self.delete_user(cognito)

        self.create_user(cognito, new_username, email, password)

    def delete_user(self, cognito):
        # cognito.authenticate(password=password)
        cognito.admin_delete_user()

    def change_password(self, cognito, username, old_password, new_password):
        cognito.authenticate(password=old_password)
        cognito.change_password(old_password, new_password)
        # cognito.client.admin_set_user_password(UserPoolId=os.getenv("AWS_COGNITO_USER_POOL_ID"),
        #                                        Username=username,
        #                                        Password=new_password,
        #                                        Permanent=True)

    def cog_test_authenticate(self):
        cognito = Cognito('us-east-1_V2t2miGey', '3nlvl0p7duau88cbbmd3pv337o',
                          user_pool_region='us-east-1',
                          client_secret='4q67ap5cb1msfci67v5p7bgv3buam78mvvhcbbmgq9va9konod4',
                          username='nauge1')

        # cognito = Cognito('us-east-1_iWsiqRN3n', '4stcts76mik8nvc1rjef5s3c3p',
        #                   user_pool_region='us-east-1',
        #                   client_secret='5n2kp1j7p818hril9eqcmgsqqjqedfgou544rrf9qjk29dkispm',
        #                   username='rishirbansal@gmail.com')

        # cognito = Cognito('us-east-1_V2t2miGey', '3nlvl0p7duau88cbbmd3pv337o',
        #                   user_pool_region='us-east-1',
        #                   client_secret='4q67ap5cb1msfci67v5p7bgv3buam78mvvhcbbmgq9va9konod4')

        # Registration
        # cognito.add_base_attributes(email='rishirbansal@gmail.com')
        #
        # cognito.register('nauge1', 'Nauge009#')
        #
        # cognito.admin_confirm_sign_up(username='nauge1')

        # Authentication
        cognito.authenticate(password='Nauge009#')

        access_token = cognito.access_token
        id_token = cognito.id_token
        refresh_token = cognito.refresh_token

        user = cognito.get_user(attr_map={"email": "email"})
        user_emnail = user._data['email']

        # Delete User
        # cognito.authenticate(password='Nauge009#')
        # cognito.delete_user()

        self.logger.debug("Cognito:")
