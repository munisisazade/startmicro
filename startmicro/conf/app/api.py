producer = """
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
