from datetime import datetime, date, timedelta, time

from cmath import phase, rect
from math import degrees, radians

import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta

# 07/28 06:02PM
human_format_datetime_1 = "%m/%d %I:%M%p"
human_format_datetime_formatter = "{:%m/%d %I:%M%p}"

# "2020-11-11"
yyyy_mm_dd_format_1 = "%Y-%m-%d"
# there's prob a more elegant way of doing this, just a little bit busy to think it out ...
yyyy_mm_dd_formatter = "{:%Y-%m-%d}"

# 2020/11/11"
yyyy_mm_dd_format_2 = "%Y/%m/%d"


def convert_timedelta_to_minutes(value: timedelta):
    seconds = value.total_seconds()
    minutes = seconds // 60
    return minutes


def get_today_formatted_backslash():
    # 2020/11/11"
    return date.today().strftime(yyyy_mm_dd_format_2)


def get_today_formatted_api_format():
    return date.today().strftime(yyyy_mm_dd_format_1)


def format_datetime_to_human_readable(value, date_format=human_format_datetime_1):
    pretty_format = value.strftime(date_format)
    return pretty_format


def parse_datetime_string(input):
    """ Simple wrapper, just because I can use this utilities easier than remembering all the different ways to call the parser"""
    result = parser.parse(input)
    return result


def print_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)


def get_utc_now():
    utc_now = datetime.now(tz=pytz.UTC)
    return utc_now


def get_utc_date():
    now = get_utc_now()
    return now.date()


def get_time_relative_units_ago(time, **kwargs):
    result = time - relativedelta(**kwargs)
    return result


def get_time_relative_units_forward(time, **kwargs):
    """
    if a datetime is passed, returns datetime
    if a date is passed, returns a date
    """
    result = time + relativedelta(**kwargs)
    return result


def get_utc_time_relative_units_ago(**kwargs):
    if len(kwargs) != 1:
        raise TypeError("This Function Only Accepts One Type")

    utc_now = get_utc_now()
    result = utc_now - relativedelta(**kwargs)
    return result


def get_utc_date_relative_units_ago(**kwargs):
    if len(kwargs) != 1:
        raise TypeError("This Function Only Accepts One Type")

    result = get_utc_date() - relativedelta(**kwargs)
    return result


def mean_angle(deg):
    return degrees(phase(sum(rect(1, radians(d)) for d in deg) / len(deg)))


def convert_time_to_seconds(value: time):
    minute = value.minute
    hour = value.hour

    seconds = minute * 60 + hour * 3600
    return seconds


def mean_time(times):
    """ copied from https://rosettacode.org/wiki/Averages/Mean_time_of_day#Python """
    """ takes a list of datetime.time (aka, no dates) """

    seconds = [convert_time_to_seconds(item) for item in times]

    day = 24 * 60 * 60
    to_angles = [s * 360.0 / day for s in seconds]
    mean_as_angle = mean_angle(to_angles)
    mean_seconds = mean_as_angle * day / 360.0
    if mean_seconds < 0:
        mean_seconds += day
    h, m = divmod(mean_seconds, 3600)
    m, s = divmod(m, 60)

    return time(int(h), int(m), int(s))
