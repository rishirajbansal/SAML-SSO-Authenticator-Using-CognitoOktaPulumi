"""
WSGI config for authenticator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Configure dotenv for environment variables

env_file = os.environ.get('ENV_FILE')
project_envs_folder = os.path.expanduser('envs/')
load_dotenv(os.path.join(project_envs_folder, env_file))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv("DJANGO_SETTINGS"))

application = get_wsgi_application()

# Load application after initializing application variable else, it will throw App aren't loaded yet error

# Load application on Start-up

from application.generic.init.initConfigurator import *
from application.generic.base.exception.serviceExceptions import InitException
import logging

logger = logging.getLogger(__name__)

try:
    init_config = InitConfigurator()
    flag = init_config.initialize()

    if not flag:
        logger.error("GenericConfig Failed to initialize prerequisites properties from InitConfigurator. System will "
                     "be terminated.")
        sys.exit(0)
    else:
        logger.info("GenericConfig initialized prerequisites properties successfully from InitConfigurator.")

except InitException as initEx:
    logger.error("InitException occurred during initializing the application. Problem occurred in InitConfigurator : ",
                 initEx)
except Exception as ex:
    logger.error("Exception occurred during initializing the application : ", str(ex))
