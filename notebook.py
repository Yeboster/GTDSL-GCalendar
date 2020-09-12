# %%
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, date, tzinfo
from gcalendar.gcalendar import GCalendar

# %%
load_dotenv()
CALENDAR_ID = getenv("CALENDAR_ID")
PICKLE_PATH = getenv("GTOKEN_PICKLE_PATH")
TIMEZONE = getenv("GTIMEZONE")
CREDENTIALS_PATH = getenv("GCREDENTIALS_PATH")
assert CALENDAR_ID is not None

# %%
calendar = GCalendar(
    CALENDAR_ID,
    pickle_path=PICKLE_PATH,
    credentials_path=CREDENTIALS_PATH,
    timezone=TIMEZONE,
)

# %%
# Get list events
dates = []
for event in calendar.get_events():
    dates.append(event["created"])
    if "summary" in event:
        print(event["summary"])
    else:
        print(event)

print(sorted(dates))

# %%
# Find event with summary
# summary = "Review recalling facts"
summary = "masterclass"
not_before_days = 40
event = calendar.find_event_with(summary=summary, not_before_days=not_before_days)
print(event)


# %%
# Get calendar list
for cal in calendar.get_calendars():
    summary = cal["summary"]
    print(summary)

    if summary.lower() == "primary":
        print(cal)

# %%
# Get events
# # %%
# print("Add a test event at 21/8/2020")
# test_date = date(2020, 8, 21)
# calendar.insert_event('Test event', start_date=test_date,
#                       description="Test description")

# # %%
# print("Add a test event at 21/8/2020 23:00 - 00:00")
# test_startdate = datetime(2020, 8, 21, 23, 0, 0)
# test_enddate = datetime(2020, 8, 21, 0, 0, 0)
# calendar.insert_event('Test event', start_datetime=test_startdate, end_datetime=test_enddate,
#                       description="Test description")

# # %%
# print("Add time repetition recurring event: 22/8/2020 15-15:30")

# test_startdate = datetime(2020, 8, 22, 15, 0, 0)
# test_enddate = datetime(2020, 8, 22, 15, 30, 0)
# calendar.insert_time_repetition_event('Test event', start_datetime=test_startdate, end_datetime=test_enddate,
#                       description="Test description")

# %%

# %%
