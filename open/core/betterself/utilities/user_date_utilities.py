from datetime import datetime

from django.http import Http404


def serialize_date_to_user_localized_date(date, user):
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
