from typing import *
from functools import wraps
from flask import make_response
from flask.globals import request

from flask.wrappers import Response
from gcalendar.gcalendar import GCalendar
from flask.app import Flask
from flask import jsonify
from werkzeug.utils import redirect


api = Flask(__name__)


def configure(gcalendar: GCalendar) -> Flask:
    api.config["gcalendar"] = gcalendar

    return api


def json_response(obj):
    response = make_response(jsonify(obj), 200)
    response.headers["content-type"] = "application/json"

    return response


def gcalendar(f):
    @wraps(f)
    def decorator():
        if "gcalendar" in api.config:
            gcalendar = api.config["gcalendar"]
            return f(gcalendar)
        else:
            return "Missing gcalendar in flask config"

    return decorator


@api.route("/")
@gcalendar
def index(gcalendar: GCalendar):

    body = "Google calendar API wrapper"

    return body


@api.route("/api/events")
@gcalendar
def events(gcalendar: GCalendar):

    args = request.args
    if "summary" in args:
        summary = args.get("summary")
        description = args.get("description") if "description" in args else None
        range_days = args.get("range_days") if "range_days" in args else 30

        response = gcalendar.find_events_with(
            summary=summary, description=description, not_before_days=range_days
        )
    else:
        response = gcalendar.get_events()

    return json_response(response)