"""
Usage:
  manage.py createSuperCogUser --username foo --password foo --email foo@foo.foo
"""

import logging

from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError, BaseCommand

from application.authenticate.integration.cognito.facade.userManagement import CognitoUserMgmt
from application.generic.base.constants.exceptionConstants import ExceptionConstants
from application.generic.base.exception.businessExceptions import CognitoUserMgmtException
from application.generic.base.exception.exceptionUtility import ExceptionUtility


class Command(createsuperuser.Command):
    logger = logging.getLogger(__name__)

    help = 'Create a superuser in Djnago Admin along with Cogntio User Pool'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None, help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        database = options.get('database')
        password = options.get('password')
        username = options.get('username')
        email = options.get('email')

        if not password or not username or not email:
            raise CommandError("--email --username and --password are required options")

        user_data = {
            'username': username,
            'password': password,
            'email': email,
        }

        self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)

        if options.get('verbosity', 0) >= 1:
            self.stdout.write("Superuser created successfully.")

        # Create User in Cogntio User Pool
        try:
            cognitoUserMgmt = CognitoUserMgmt()

            cognitoUserMgmt.cog_create_user(username, username, password)

            self.logger.debug("User is created in Cognito Successfully.")

        except CognitoUserMgmtException as cogEx:
            self.logger.error("CognitoUserMgmtException occurred in while saving user in Admin Model : {}".
                              format(cogEx.message))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_COGNITO_USER_MGMT_EXCEPTION,
                                                       ExceptionConstants.USERMESSAGE_COGNITO_USER_MGMT_EXCEPTION,
                                                       cogEx.message,
                                                       CognitoUserMgmtException.__name__)
