# %%
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, date
import app

# %%
load_dotenv()
CALENDAR_ID = getenv('CALENDAR_ID')
assert CALENDAR_ID is not None

# %%
calendar = app.Calendar(CALENDAR_ID)

# %%
# Get calendar list
for cal in calendar.get_calendars():
    summary = cal['summary']
    print(summary)

    if summary.lower() == "primary":
        print(cal)

# # %%
# # Add a test event at 21/8/2020
# test_date = date(2020, 8, 21)
# calendar.insert_event('Test event', date=test_date,
#                       description="Test description")

# # %%
# # Add a test event at 21/8/2020 23:00 - 00:00
# test_startdate = datetime(2020, 8, 21, 23, 0, 0)
# test_enddate = datetime(2020, 8, 21, 0, 0, 0)
# calendar.insert_event('Test event', start_datetime=test_startdate, end_datetime=test_enddate,
#                       description="Test description")

# %%
print("Add time repetition recurring event")

test_startdate = datetime(2020, 8, 22, 15, 0, 0)
test_enddate = datetime(2020, 8, 22, 15, 30, 0)
calendar.insert_time_repetition_event('Test event', start_datetime=test_startdate, end_datetime=test_enddate,
                      description="Test description")
