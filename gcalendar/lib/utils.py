import logging
from flask import make_response
from flask import jsonify


def json_response(obj):
    response = make_response(jsonify(obj), 200)
    response.headers["content-type"] = "application/json"

    return response


def success_response(obj):
    res = {"status": "success", "data": obj}

    return json_response(res)


def error_response(message: str):
    res = {"status": "error", "message": message}

    logging.error(f"API error: {message}")

    return json_response(res)
