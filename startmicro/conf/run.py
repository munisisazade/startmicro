run = """
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
