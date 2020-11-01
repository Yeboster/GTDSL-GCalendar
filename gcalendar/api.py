from typing import *
from functools import wraps
from flask import make_response

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
def index(gcalendar: Optional[GCalendar]):

    body = "Google calendar API wrapper"

    return body


@api.route("/api/events")
@gcalendar
def events(gcalendar: Optional[GCalendar]):

    response = gcalendar.get_events() if gcalendar else "Gcalendar not configured"

    return json_response(response)