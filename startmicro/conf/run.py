run_restful = """
import os
import traceback

from flask import request, jsonify
from app import create_app
from app.utils import PageNotFound, MethodNotAllowed, Error
from app.utils.logger import log
from app.api.producer import micro_api

app = create_app()

app.register_blueprint(micro_api)


# error handling
@app.errorhandler(404)
def page_not_found(e):
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(",")[0]
    else:
        ip = request.remote_addr
    log.error("Page not found at {} {} {}".format(request.path, request.method, ip))
    return jsonify(PageNotFound().serialize()), 404


# error handling
@app.errorhandler(405)
def method_not_allowed(e):
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(",")[0]
    else:
        ip = request.remote_addr
    log.error("Method not allowed at {} {} {}".format(request.path, request.method, ip))
    return jsonify(MethodNotAllowed().serialize()), 405


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    log.fatal(f"{tb}")
    return jsonify(Error(status=500, description="ERROR", message={"message": "Unknown error"}).serialize()), 500


if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))

"""

run_redis_pubsub = """
import os
from redisrpc import RedisRPC
from app.api.producer import handler
from dotenv import load_dotenv

load_dotenv()  # load common environment
load_dotenv(dotenv_path='config/{}.env'.format(os.getenv("APP_SETTINGS"))) # load configs

# Listen `microservice` channels accept all messages from this channel
rpc = RedisRPC("microservice")

# Register your data handlers here
rpc.register(handler, "handler")


if __name__ == '__main__':
    rpc.listen() # pubsub have no port

"""

run_rabbitmq = """
import os
import json
import pika
from app.api.producer import handler
from dotenv import load_dotenv

load_dotenv()  # load common environment
load_dotenv(dotenv_path='config/{}.env'.format(os.getenv("APP_SETTINGS"))) # load configs

RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')
RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT')


print("Rabbitmq RPC server start")
# Connect to channel
credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='microservice', durable=True)


# Data handler all requests
def on_request(ch, method, props, body):
    response = json.dumps(handler(body))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Accept from channel
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='microservice')
channel.start_consuming()

"""
