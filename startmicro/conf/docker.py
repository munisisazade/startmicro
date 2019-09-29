Dockerfile = """
FROM python:3.6

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /code
# Copy in your requirements file
ADD requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.
RUN pip install virtualenvwrapper
RUN python3 -m venv /venv
RUN /venv/bin/pip install -U pip
RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}
ADD . ${APP_ROOT}

# uWSGI will listen on this port
EXPOSE 5510


# Start flask app
CMD [ "/venv/bin/python", "run.py"]

"""

docker_compose = """
version: "3"

services:

  microservice:
    container_name: micro
    restart: "always"
    build: .
    environment:
      - VIRTUAL_HOST=example.com
      - VIRTUAL_PORT=5000
    volumes:
      - .:/code
      
"""

redis_dockerfile = """
FROM redis:4.0.11

ENV REDIS_PASSWORD {}

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]

"""

redis_docker_compose = """
version: '3'

services:

  redis:
    build:
      context: .
      dockerfile: redis.dockerfile
    restart: "always"
    container_name: redis
    ports:
      - 6379:6379
    volumes:
      - ./redisdb:/var/lib/redis
    # env_file: .env # if have dotenv file
     
"""

rabbit_docker_compose = """
version: '3'

services:
  
  rabbitmq:
    image: "rabbitmq:3-management"
    hostname: "localhost"
    container_name: rabbit
    environment:
      RABBITMQ_ERLANG_COOKIE: "SWQOKODSQALRPCLNMEQG"
      RABBITMQ_DEFAULT_USER: "rabbitmq"
      RABBITMQ_DEFAULT_PASS: "rabbitmq"
      RABBITMQ_DEFAULT_VHOST: "/"
    ports:
      - "15672:15672"
      - "5672:5672"
    labels:
      NAME: "localhost"
    volumes:
      - "./enabled_plugins:/etc/rabbitmq/enabled_plugins"

"""

rabbit_enable_plugins = """
[rabbitmq_management, rabbitmq_management_visualiser].
"""
