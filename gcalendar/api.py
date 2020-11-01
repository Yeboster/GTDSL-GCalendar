from datetime import datetime
from logging import error
from typing import *
from functools import wraps
from flask import make_response, json
from flask.globals import request

from gcalendar.gcalendar import GCalendar
from flask.app import Flask
from flask import jsonify


api = Flask(__name__)


def configure(gcalendar: GCalendar) -> Flask:
    api.config["gcalendar"] = gcalendar

    return api


def json_response(obj):
    response = make_response(jsonify(obj), 200)
    response.headers["content-type"] = "application/json"

    return response


def success_response(obj):
    res = {"status": "success", "data": obj}

    return json_response(res)


def error_response(message: str):
    res = {"status": "error", "message": message}

    return json_response(res)


def gcalendar(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "gcalendar" in api.config:
            gcalendar = api.config["gcalendar"]
            return f(gcalendar, *args, **kwargs)
        else:
            return "Missing gcalendar in flask config"

    return decorator


@api.route("/")
@gcalendar
def index(gcalendar: GCalendar):

    body = "Google calendar API wrapper"

    return body


@api.route("/api/events", methods=["GET"])
@gcalendar
def events(gcalendar: GCalendar):

    args = request.args
    if "summary" in args or "description" in args or "range_days" in args:
        summary = args.get("summary") if "summary" in args else None
        description = args.get("description") if "description" in args else None
        if "days_range" in args:
            try:
                days_range = int(args.get("days_range"))
            except:
                return error_response("Cannot parse days_range")
        else:
            days_range = 30

        events = gcalendar.find_events_with(
            summary=summary, description=description, not_before_days=days_range
        )
    else:
        events = gcalendar.get_events()

    return success_response(events)


@api.route("/api/events/<id>", methods=["GET"])
@gcalendar
def event(gcalendar: GCalendar, id: str):
    try:
        event = gcalendar.get_event(id)

        return success_response(event)
    except Exception as e:
        message = str(e)
        return error_response(f"Cannot get event. Reason: {message}")


@api.route("/api/events", methods=["POST"])
@gcalendar
def insert_event(gcalendar: GCalendar):
    body = None
    try:
        body = json.loads(request.data)
    except:
        return error_response("Json not valid")

    if body:
        try:
            title = body["title"]
            start_date = datetime.fromisoformat(body["start_date"])
            end_date = datetime.fromisoformat(body["end_date"])
            description = body["description"] if "description" in body else None

            args = request.args
            insert_fun = (
                gcalendar.insert_time_repetition_event
                if "time_repetition" in args
                else gcalendar.insert_event
            )

            event = insert_fun(
                title, start_date=start_date, end_date=end_date, description=description
            )

            return success_response(event)
        except Exception as e:
            message = str(e)
            return error_response(f"Cannot insert event. Reason: {message}")


@api.route("/api/events/<id>", methods=["DELETE"])
@gcalendar
def delete_event(gcalendar: GCalendar, id: str):
    try:
        res = gcalendar.delete_event(id)
        return success_response(res)
    except Exception as e:
        message = str(e)
        return error_response(f"Cannot delete event. Reason: {message}")
