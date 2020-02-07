from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class AuthenticateConfig(AdminConfig):
    #name = 'application.authenticate'
    default_site = 'application.authenticate.admin.CognitoAdmin'
