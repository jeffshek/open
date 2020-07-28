from datetime import datetime

import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta

# 07/28 06:02PM
human_format_1 = "{:%m/%d %I:%M%p}"


def format_datetime_to_human_readable(value):
    pretty_format = human_format_1.format(value)
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
