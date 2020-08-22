from os import getenv

from dotenv import load_dotenv

from lib.calendar import Calendar




if __name__ == '__main__':
    load_dotenv()

    CALENDAR_ID = getenv('CALENDAR_ID')
    TIMEZONE = getenv('TIMEZONE')

    if CALENDAR_ID:
        calendar = Calendar(CALENDAR_ID, TIMEZONE)
