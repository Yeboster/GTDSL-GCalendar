#!/usr/bin/env python3

import logging
from os import getenv

from dotenv import load_dotenv

from gcalendar.api import api, configure
from gcalendar.gcalendar import GCalendar


if __name__ == "__main__":
    load_dotenv()

    GCALENDAR_ID = getenv("GCALENDAR_ID")
    GTIMEZONE = getenv("GTIMEZONE")

    app = api
    if GCALENDAR_ID:
        gcalendar = GCalendar(GCALENDAR_ID, timezone=GTIMEZONE)
        app = configure(gcalendar)
    else:
        logging.warn("[!] Missing envs")

    # TODO: In production use WSGI
    app.run()