from __future__ import print_function

import os.path
import pickle
from datetime import date, datetime, timedelta
from os import getenv
from os.path import expanduser
from typing import *

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate():
    """Authenticate and return the api object"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


# Unfortunately Google Calendar API is a dynamic object, so no intelli-sense
class Calendar():
    """A wrapper to interact with Google Calendar"""

    def __init__(self, calendar_id: str, timezone: str = None) -> None:
        self.service = authenticate()
        self.id = calendar_id
        self.timezone = timezone if timezone else "Europe/Rome"

    def get_calendars(self) -> List[Dict[str, Any]]:
        calendars = self.service.calendarList().list(  # pylint: disable=maybe-no-member
        ).execute()

        return calendars['items']

    def get_events(self) -> List[Dict[str, Any]]:
        events = self.service.events().list().execute() # pylint: disable=maybe-no-member

        return events['items']

    def insert_event(self, title: str, *, date: date = None, start_datetime: datetime = None, end_datetime: datetime = None, description: str = None) -> None:
        """Insert event into calendar"""
        body: Dict[str, Any] = {}
        body['summary'] = title

        if date:
            body['start'] = dict(date=date.isoformat())
            body['end'] = dict(date=date.isoformat())
        elif start_datetime:
            time_zone = 'Europe/Rome'
            body['start'] = dict(
                dateTime=start_datetime.isoformat(), timeZone=time_zone)
            if end_datetime:
                body['end'] = dict(
                    dateTime=end_datetime.isoformat(), timeZone=time_zone)
            else:
                end_datetime = start_datetime + timedelta(hours=1)
                body['end'] = dict(
                    dateTime=end_datetime.isoformat(), timeZone=time_zone)
        else:
            raise Exception('No date was passed')

        if description:
            body['notes'] = description

        self.service.events().insert(calendarId=self.id,  # pylint: disable=maybe-no-member
                                     body=body).execute()

    def insert_time_repetition_event(self, title: str, *, date: date = None, start_datetime: datetime = None, end_datetime: datetime = None, description: str = None) -> None:
        """Insert into calendar event with repeatition of 1 hour, 1 day, 1 week, 1 month"""
        time_repetition = [1,7,30]

        recurring_dates: List[Tuple[Any,Any]] = []
        if date:
           recurring_dates += [(date + timedelta(days=d), None) for d in time_repetition]
        elif start_datetime:
            # TODO: Check if recurringId can be used, to create recurring events
            def add_to_endtime(**kwargs):
                end_datetime + timedelta(**kwargs) if end_datetime else None

            recurring_dates += [(start_datetime, add_to_endtime(hours=1))]
            recurring_dates += [(start_datetime + timedelta(days=d), add_to_endtime(days=d)) for d in time_repetition]
        else:
            raise Exception('No date was passed')

        for start, end in recurring_dates:
            if type(start) is date:
                self.insert_event(title, date=start, description=description)
            else:
                self.insert_event(title, start_datetime=start, end_datetime=end, description=description)




if __name__ == '__main__':
    load_dotenv()

    CALENDAR_ID = getenv('CALENDAR_ID')
    TIMEZONE = getenv('TIMEZONE')

    if CALENDAR_ID:
        calendar = Calendar(CALENDAR_ID, TIMEZONE)
