#!/usr/bin/env python3

from os import getenv

from dotenv import load_dotenv

from gcalendar.gcalendar import GCalendar


if __name__ == "__main__":
    load_dotenv()

    GCALENDAR_ID = getenv("GCALENDAR_ID")
    GTIMEZONE = getenv("GTIMEZONE")

    if GCALENDAR_ID:
        gcalendar = GCalendar(GCALENDAR_ID, GTIMEZONE)
