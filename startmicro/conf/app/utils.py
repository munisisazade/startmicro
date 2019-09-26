utils_init = """
from .response import Success, Error, PageNotFound, MethodNotAllowed

"""

response = """
import uuid
from datetime import datetime
import os


class Response(object):
    APP_NAME = os.getenv("INSTANCE_NAME")

    def __init__(self, status, description, message, transaction=None):
        self.status = status
        self.description = description
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.transaction = str(uuid.uuid4()) if not transaction else transaction
        self.app_name = self.APP_NAME
        self.message = message


class Success(Response):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            'timestamp': self.timestamp,
            'status': self.status,
            'description': self.description,
            'transaction': self.transaction,
            'exception': None,
            'app_name': self.app_name,
            'data': self.message
        }


class Error(Response):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return {
            'timestamp': self.timestamp,
            'status': self.status,
            'description': self.description,
            'transaction': self.transaction,
            'exception': self.message,
            'app_name': self.app_name,
            'data': None
        }


class PageNotFound(Error):
    def __init__(self):
        context = {}
        context["status"] = 404
        context["description"] = "Not found Error"
        context["message"] = {
            "status": 404,
            "message": "Url not found"
        }
        super().__init__(**context)


class MethodNotAllowed(Error):
    def __init__(self):
        context = {}
        context["status"] = 405
        context["description"] = "Method Not Allowed"
        context["message"] = {
            "status": 405,
            "message": "Method Not Allowed"
        }
        super().__init__(**context)


class UnknownError(Error):
    def __init__(self):
        context = {}
        context["status"] = 500
        context["description"] = "Unknown Error"
        context["message"] = {
            "status": 500,
            "message": "Unknown Error"

        }
        super().__init__(**context)

"""

logger = """
import json
import os
from datetime import datetime
from inspect import getframeinfo, stack

LOG_LEVELS = [
    "FATAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG"
]


class BridgeLogger(object):
    log_file = os.getenv("LOG_FILE_PATH")

    @classmethod
    def get_format(cls, info, level, msg):
        log_data = {
            "app": os.getenv("INSTANCE_NAME"),
            "@timestamp": datetime.now().isoformat(),
            "level": level,
            "function": info.function,
            "file": info.filename.split('/')[-1],
            "line": info.lineno,
            "message": str(msg)
        }
        return json.dumps(log_data)

    @classmethod
    def error(cls, msg):
        caller = getframeinfo(stack()[1][0])
        data = cls.get_format(caller, LOG_LEVELS[1], msg)
        cls.__write(data)

    @classmethod
    def fatal(cls, msg):
        caller = getframeinfo(stack()[1][0])
        data = cls.get_format(caller, LOG_LEVELS[0], msg)
        cls.__write(data)

    @classmethod
    def warning(cls, msg):
        caller = getframeinfo(stack()[1][0])
        data = cls.get_format(caller, LOG_LEVELS[2], msg)
        cls.__write(data)

    @classmethod
    def info(cls, msg):
        caller = getframeinfo(stack()[1][0])
        data = cls.get_format(caller, LOG_LEVELS[3], msg)
        cls.__write(data)

    @classmethod
    def debug(cls, msg):
        caller = getframeinfo(stack()[1][0])
        data = cls.get_format(caller, LOG_LEVELS[4], msg)
        cls.__write(data)

    @classmethod
    def __write(cls, data):
        print(data)
        with open(cls.log_file, "a") as file:
            file.write(f"{data}\\n")


log = BridgeLogger

"""
