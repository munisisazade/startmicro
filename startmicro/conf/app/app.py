
app_init = """
from flask_api import FlaskAPI

from instance.config import Config


def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(Config())
    return app

"""
