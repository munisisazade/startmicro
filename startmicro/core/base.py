import os
import sys
import subprocess
from startmicro.conf.app.api import producer_restful, producer_redis, producer_rabbitmq
from startmicro.conf.app.app import app_init
from startmicro.conf.run import run_restful, run_redis_pubsub, run_rabbitmq
from startmicro.conf.readme import readme
from startmicro.conf.docker import docker_compose, Dockerfile
from startmicro.conf.requirements import requirement_list
from startmicro.conf.dotenv import env, dev_env, test_env, stage_env, prod_env
from startmicro.conf.instance_py.config import config
from startmicro.conf.exaples import redis_client, rabbit_client, redis_credentials, rabbitmq_credentials, \
    redis_required, rabbit_required
from startmicro.conf.app.utils import logger, response, utils_init
from startmicro.core.utils.questions import prompt, style, questions
from startmicro.core.utils.detect import os_type


class Command(object):
    """
        Application base logic class
    """

    def __init__(self, folder_name):
        """
            Initialize folder name
        """
        self.folder_name = folder_name
        self.slash = "/" if os_type != "Windows" else "\\"
        self.path = "{}{}".format(folder_name, self.slash)
        self.app = "{}app".format(self.path)
        self.api_path = "{}{}api".format(self.app, self.slash)
        self.utils_path = "{}{}utils".format(self.app, self.slash)
        self.instance = "{}instance".format(self.path)
        self.config = "{}config".format(self.path)
        self.answer = None

    def run(self):
        self.create_folder()  # Create application Folder
        # First Create virtualenv folder
        answers = prompt(questions, style=style)
        print("ANSWERS: ===> ", answers)
        self.answer = answers
        self.create_virtualenv()
        self.main_structure()
        self.write_file(self.app, "__init__.py", app_init)
        self.write_file(self.utils_path, "__init__.py", utils_init)
        self.write_file(self.utils_path, "logger.py", logger)
        self.write_file(self.utils_path, "response.py", response)
        self.write_file(self.instance, "config.py", config)
        self.make_env()
        self.write_file(self.folder_name, "requirements.txt", requirement_list)
        self.write_file(self.folder_name, "docker-compose.yml", docker_compose)
        self.write_file(self.folder_name, "Dockerfile", Dockerfile)
        self.write_file(self.folder_name, "README.md", readme)
        if answers.get("type") == "Restful" or not answers:
            self.write_file(self.api_path, "producer.py", producer_restful)
            self.write_file(self.folder_name, "run.py", run_restful)
        elif answers.get("type") == "Redis pubsub":
            self.write_file(self.api_path, "producer.py", producer_redis)
            self.write_file(self.folder_name, "run.py", run_redis_pubsub)
            self.write_file(self.folder_name, "redis_client.py", redis_client)
            self.add_env(redis_credentials)
            self.update_file(self.folder_name, "requirements.txt", redis_required)
        elif answers.get("type") == "Rabbitmq RPC":
            self.write_file(self.api_path, "producer.py", producer_rabbitmq)
            self.write_file(self.folder_name, "run.py", run_rabbitmq)
            self.write_file(self.folder_name, "rabbit_client.py", rabbit_client)
            self.add_env(rabbitmq_credentials)
            self.update_file(self.folder_name, "requirements.txt", rabbit_required)

    def make_env(self):
        self.write_file(self.folder_name, ".env", env)
        self.write_file(self.config, "dev.env", dev_env)
        self.write_file(self.config, "test.env", test_env)
        self.write_file(self.config, "stage.env", stage_env)
        self.write_file(self.config, "prod.env", prod_env)

    def add_env(self, data):
        self.update_file(self.config, "dev.env", data)
        self.update_file(self.config, "test.env", data)
        self.update_file(self.config, "stage.env", data)
        self.update_file(self.config, "prod.env", data)

    def write_file(self, path, filename, data):
        with open("{}{}{}".format(path, self.slash, filename), "w") as file:
            file.write(data.lstrip())

    def update_file(self, path, filename, data):
        with open("{}{}{}".format(path, self.slash, filename), "a") as file:
            file.write(data.lstrip())

    def main_structure(self):
        os.makedirs(self.app)
        self.make_init(self.app)
        os.makedirs(self.api_path)
        self.make_init(self.api_path)
        os.makedirs(self.utils_path)
        self.make_init(self.utils_path)
        os.makedirs(self.instance)
        self.make_init(self.instance)
        os.makedirs(self.config)

    def create_virtualenv(self):
        """
            Creating virtualenviroment
        """
        sys.stdout.write("Creating virtualenviroment\n")
        path = "virtualenv -p python3 {}.venv".format(self.path)
        if os_type == "Windows":
            self.run_win_cmd(path.replace("3", ""))
        else:  # Mac or Linux
            subprocess.call(path, shell=True)

    def make_init(self, path):
        with open("{}{}__init__.py".format(path, self.slash), "a") as file:
            file.write("")

    def run_win_cmd(self, commands):
        result = []
        process = subprocess.Popen(commands,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for line in process.stdout:
            result.append(line)
        errcode = process.returncode
        for line in result:
            sys.stdout.write(line.decode("utf-8"))
        if errcode is not None:
            raise Exception('cmd %s failed, see above for details', commands)

    def create_folder(self):
        os.makedirs(self.folder_name)
