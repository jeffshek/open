from datetime import datetime
import pytz


def print_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)


def get_utc_now():
    utc_now = datetime.now(tz=pytz.UTC)
    return utc_now
