config = """
import os
from dotenv import load_dotenv

load_dotenv()  # load common environment
load_dotenv(dotenv_path='config/{}.env'.format(os.getenv("APP_SETTINGS"))) # load configs


def env_to_python(string):
    # Convert strings to python object
    if string == "False":
        return False
    elif string == "True":
        return True
    else:
        return string


class Config(object):
    DEBUG = env_to_python(os.getenv("DEBUG"))
    TESTING = env_to_python(os.getenv("TESTING"))
    CSRF_ENABLED = env_to_python(os.getenv("CSRF_ENABLED"))
    FLASK_ENV = os.getenv("FLASK_ENV")
    FLASK_APP = os.getenv("FLASK_APP")
    SECRET = os.getenv("SECRET_KEY")
    TEMPLATES_AUTO_RELOAD = env_to_python(os.getenv("TEMPLATES_AUTO_RELOAD"))
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_HEADER_TYPE = os.getenv("JWT_HEADER_TYPE")

"""
