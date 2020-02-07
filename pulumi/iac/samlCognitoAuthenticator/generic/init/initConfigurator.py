import os

from dotenv import load_dotenv


class InitConfigurator:

    def __init__(self):
        pass

    def initialize(self):
        flag = True

        print("InitConfigurator loading the application prerequisites...")

        try:
            env_file = os.environ.get('ENV_FILE')
            project_envs_folder = os.path.expanduser('../envs/')
            load_dotenv(os.path.join(project_envs_folder, env_file))

        except Exception as ex:
            print("Exception occurred during initializing the application : {}".format(ex))
            flag = False

        return flag

