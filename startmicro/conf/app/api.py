producer_restful = """
from flask import Blueprint, request, jsonify

from app.utils import Success
from app.utils.logger import log

micro_api = Blueprint('micro_api', __name__)


@micro_api.route('/', methods=['GET'])
def handler():
    # Todo base algorithm here
    log.debug("Success")
    success = Success(
        status=200,
        description="It is work!",
        message={
            "data": "Success"
        }
    )
    return jsonify(success.serialize())

"""

producer_redis = """
from app.utils import Success
from app.utils.logger import log


def handler(request):
    # Todo base algorithm here
    print("Requested data dictionary", request)
    log.debug("Success RPC data")
    success = Success(
        status=200,
        description="It is work!",
        message={
            "data": request
        }
    )
    return success.serialize() # response to client 

"""

producer_rabbitmq = """
from app.utils import Success
from app.utils.logger import log


def handler(request):
    # Todo base algorithm here
    data = json.loads(request)
    print("Requested data dictionary", data)
    log.debug("Success RPC Rabbit mq data")
    success = Success(
        status=200,
        description="It is work!",
        message={
            "data": data
        }
    )
    return success.serialize() # response to client 

"""
