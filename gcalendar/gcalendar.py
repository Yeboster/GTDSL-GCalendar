from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Tuple, Union

from .authenticate import authenticate


# Unfortunately Google Calendar API is a dynamic object, so no intelli-sense
class GCalendar:
    """A wrapper to interact with Google Calendar"""

    def __init__(
        self, calendar_id: str, pickle_path: str = None, credentials_path: str = None, timezone: str = None
    ) -> None:
        self.service = authenticate(pickle_path=pickle_path, credentials_path=credentials_path)
        self.id = calendar_id
        self.timezone = timezone if timezone else "Europe/Rome"

    def get_calendars(self) -> List[Dict[str, Any]]:
        calendars = (
            self.service.calendarList() # pylint: disable=maybe-no-member
            .list()
            .execute()
        )

        return calendars["items"]

    def get_events(self) -> List[Dict[str, Any]]:
        events = (
            self.service.events().list().execute() # pylint: disable=maybe-no-member
        )

        return events["items"]

    def insert_event(
        self,
        title: str,
        *,
        start_date: Union[date, datetime] = None,
        end_date: Union[datetime, date] = None,
        description: str = None
    ) -> None:
        """Insert event into calendar"""
        body: Dict[str, Any] = {}
        body["summary"] = title
        if start_date:

            def date_dict_of(date: Union[date, datetime]):
                iso = date.isoformat()

                dict_date = dict(date=iso)
                if type(date) is datetime:
                    dict_date = dict(dateTime=iso, timeZone=self.timezone)

                return dict_date

            body["start"] = date_dict_of(start_date)

            if end_date:
                body["end"] = date_dict_of(end_date)
            else:
                body["end"] = date_dict_of(start_date + timedelta(hours=1))
        else:
            raise Exception("No date was passed")

        if description:
            body["notes"] = description

        self.service.events().insert( # pylint: disable=maybe-no-member
            calendarId=self.id, body=body
        ).execute()

    def insert_time_repetition_event(
        self,
        title: str,
        *,
        start_date: Union[date, datetime] = None,
        end_date: Union[datetime, date] = None,
        description: str = None
    ) -> None:
        """Insert into calendar event with repeatition of 1 hour, 1 day, 1 week, 1 month"""
        time_repetition = [1, 7, 31]
        recurring_dates: List[Tuple[Any, Any]] = []

        if start_date:
            def add_to_end_date(**kwargs):
                return end_date + timedelta(**kwargs) if end_date else None

            recurring_dates += [(start_date, add_to_end_date(hours=1))]
            recurring_dates += [
                (start_date + timedelta(days=d), add_to_end_date(days=d))
                for d in time_repetition
            ]
        else:
            raise Exception("No date was passed")

        for start, end in recurring_dates:
            self.insert_event(
                title, start_date=start, end_date=end, description=description
            )