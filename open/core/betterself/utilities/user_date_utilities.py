from datetime import datetime

from django.http import Http404


def serialize_date_to_user_localized_datetime(date, user):
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise Http404

    start_period = date
    start_period = datetime(
        year=start_period.year,
        month=start_period.month,
        day=start_period.day,
        tzinfo=user.timezone,
    )
    return start_period


def serialize_end_date_to_user_localized_datetime(date, user):
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise Http404

    end_period = date
    end_period = datetime(
        year=end_period.year,
        month=end_period.month,
        day=end_period.day,
        hour=23,
        minute=59,
        second=59,
        tzinfo=user.timezone,
    )
    return end_period
