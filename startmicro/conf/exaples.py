redis_client = """
import os
from redisrpc import RedisRPC
from dotenv import load_dotenv

load_dotenv()  # load common environment
load_dotenv(dotenv_path='config/{}.env'.format(os.getenv("APP_SETTINGS"))) # load configs


rpc = RedisRPC("microservice")  # channel name must be same as server
handler = rpc.send("handler", {'data': "Hello world"})  # send data to spesific event

# response from server handlers
print(handler)
  
"""

redis_credentials = """
REDIS_URI='redis://:{}@localhost:6379/0' # you can change this
"""

redis_required = """
redis==3.3.8
redispubsub==0.0.5
"""

rabbit_client = """
import os
import pika
import uuid
import json

from dotenv import load_dotenv

load_dotenv()  # load common environment
load_dotenv(dotenv_path='config/{}.env'.format(os.getenv("APP_SETTINGS")))  # load configs

RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')
RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT')

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)


class SampleRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=credentials))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=os.getenv("RABBIT_QUEUE_NAME"),
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response)


rpc = SampleRpcClient()

print(" Sending data to Server")
response = rpc.call(json.dumps({"data": "Hello world"}))
print(" Response from server ", response)

"""
rabbitmq_credentials = """
RABBIT_USER="rabbitmq" # change this
RABBIT_PASSWORD="rabbitmq" # change this
RABBIT_HOST="localhost" # change this
RABBIT_PORT="5672" # change this
RABBIT_QUEUE_NAME="microservice" # change this
"""

rabbit_required = """
pika==1.1.0
"""
