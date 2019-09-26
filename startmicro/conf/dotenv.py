env = """
# Select enviroment dev, test, stage, prod
APP_SETTINGS="dev"
HOST="0.0.0.0"
PORT=5000
INSTANCE_NAME='microservice'
"""

dev_env = """
# Flask default conf
DEBUG=True
CSRF_ENABLED=True
TESTING=True
FLASK_ENV='development'
FLASK_APP='run.py'
TEMPLATES_AUTO_RELOAD=True
# Aditional default configs
APP_NAME='microservice1'
LOG_FILE_PATH='micro.log'
# Secrets
SECRET_KEY="q&-=9#$8a5cy297l1qkb+$8o)h(3a$2br!8tdo5iz6rb@ub2=-"
JWT_SECRET_KEY='&[`SD*}MSt6d}?W4rz76Q@d4N,)cG5Wx'  # Change this!
JWT_HEADER_TYPE='Token'  # Change this!

"""

test_env = """
# Flask default conf
DEBUG=True
CSRF_ENABLED=True
TESTING=True
FLASK_ENV='development'
FLASK_APP='run.py'
TEMPLATES_AUTO_RELOAD=True
# Aditional default configs
APP_NAME='microservice1'
LOG_FILE_PATH='micro.log'
# Secrets
SECRET_KEY="q&-=9#$8a5cy297l1qkb+$8o)h(3a$2br!8tdo5iz6rb@ub2=-"
JWT_SECRET_KEY='&[`SD*}MSt6d}?W4rz76Q@d4N,)cG5Wx'  # Change this!
JWT_HEADER_TYPE='Token'  # Change this!

"""

stage_env = """
# Flask default conf
DEBUG=False
CSRF_ENABLED=True
TESTING=False
FLASK_ENV='development'
FLASK_APP='run.py'
TEMPLATES_AUTO_RELOAD=True
# Aditional default configs
APP_NAME='microservice1'
LOG_FILE_PATH='micro.log'
# Secrets
SECRET_KEY="q&-=9#$8a5cy297l1qkb+$8o)h(3a$2br!8tdo5iz6rb@ub2=-"
JWT_SECRET_KEY='&[`SD*}MSt6d}?W4rz76Q@d4N,)cG5Wx'  # Change this!
JWT_HEADER_TYPE='Token'  # Change this!

"""

prod_env = """
# Flask default conf
DEBUG=False
CSRF_ENABLED=True
TESTING=False
FLASK_ENV='production'
FLASK_APP='run.py'
TEMPLATES_AUTO_RELOAD=True
# Aditional default configs
APP_NAME='microservice1'
LOG_FILE_PATH='micro.log'
# Secrets
SECRET_KEY="q&-=9#$8a5cy297l1qkb+$8o)h(3a$2br!8tdo5iz6rb@ub2=-"
JWT_SECRET_KEY='&[`SD*}MSt6d}?W4rz76Q@d4N,)cG5Wx'  # Change this!
JWT_HEADER_TYPE='Token'  # Change this!

"""
