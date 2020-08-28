import json
from collections import defaultdict
from datetime import datetime

import pandas as pd
from django.db.models import Sum
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.betterself.constants import PRODUCTIVITY_METRICS
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.serializers.sleep_log_serializers import (
    SleepLogReadSerializer,
)
from open.core.betterself.serializers.supplement_log_serializers import (
    SupplementLogReadSerializer,
)
from open.core.betterself.serializers.supplement_serializers import (
    SimpleSupplementReadSerializer,
)
from open.utilities.date_and_time import (
    get_time_relative_units_forward,
    mean_time,
    get_time_relative_units_ago,
    yyyy_mm_dd_format_1,
)

PRODUCTIVITY_LOG_VALUE_FIELDS = [
    "uuid",
    "date",
    "very_productive_time_minutes",
    "productive_time_minutes",
    "neutral_time_minutes",
    "distracting_time_minutes",
    "very_distracting_time_minutes",
    "pomodoro_count",
    "notes",
    "mistakes",
]


def get_overview_supplements_data(user, start_period, end_period):
    response = {
        "start_period": start_period.date().isoformat(),
        "end_period": end_period.date().isoformat(),
        # group across each day and what supplements were taken
        # hence, this will be called "daily" logs
        "daily_logs": defaultdict(list),
        # group by supplements and how many were taken
        "summary": [],
        "total_quantity": 0,
    }

    supplement_logs = SupplementLog.objects.filter(
        user=user, time__lte=end_period, time__gte=start_period
    ).order_by("time")
    if not supplement_logs.exists():
        return response

    for log in supplement_logs:
        # otherwise everything is stored on the UTC date for the user, which doesn't make as much sense
        user_timezone = user.timezone
        normalized_time = user_timezone.normalize(log.time)
        log_date = normalized_time.date().isoformat()

        serialized_log = SupplementLogReadSerializer(log).data
        response["daily_logs"][log_date].append(serialized_log)

    # aggregate all the supplement logs, sort them by the name, and then count how many were used
    taken_data = (
        supplement_logs.values("supplement__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by()
    )

    for value in taken_data:
        taken_result = {}

        supplement = Supplement.objects.get(name=value["supplement__name"], user=user)
        supplement_serialized = SimpleSupplementReadSerializer(supplement).data
        taken_result["supplement"] = supplement_serialized

        # add the individual total quantity to the aggregrate
        response["total_quantity"] += value["total_quantity"]

        # decimal has to be showed as string for json
        taken_result["quantity"] = str(value["total_quantity"])

        response["summary"].append(taken_result)

    return response


def get_overview_productivity_data(
    user, start_period: datetime, end_period: datetime, lookback_periods: int = 14
):
    LOG_MODEL = DailyProductivityLog

    response = {
        "start_period": start_period.date().isoformat(),
        "end_period": end_period.date().isoformat(),
        "logs": [],
    }

    # get more data, that way we can calculate a running historical average
    start_period_with_lookback = get_time_relative_units_ago(
        start_period, days=lookback_periods
    )

    logs = LOG_MODEL.objects.filter(
        user=user, date__lte=end_period, date__gte=start_period_with_lookback
    ).order_by("date")
    if not logs.exists():
        return response

    df = pd.DataFrame.from_records(
        logs.values(*PRODUCTIVITY_LOG_VALUE_FIELDS), index="date"
    )
    df.index = pd.DatetimeIndex(df.index)

    formatted_dates = [item.strftime(yyyy_mm_dd_format_1) for item in df.index.date]
    df["date"] = formatted_dates

    # use this to truncate the resampled series
    original_index = df.index

    df["uuid"] = df["uuid"].astype(str)
    df = df.resample("D").first()

    # for metric in DailyProductivityLog.PRODUCTIVITY_METRICS:
    for metric in PRODUCTIVITY_METRICS:
        # create a new column on the df with the rolling_mean
        metric_mean_label = f"{metric}_mean"
        mean_series = df[metric].rolling(window=lookback_periods, min_periods=1).mean()
        df[metric_mean_label] = mean_series

    # now after we've calculated a bunch of rolling averages, truncate the missing days?
    # alternatively, maybe i don't do this and show the nan on missing charts, not sure yet
    df = df.loc[original_index]

    # just always make sure it's sorted by the ascending datetime
    df = df.sort_index()

    # truncate all the previous records you needed for rolling averages, use date() to remove tz info
    df = df.loc[start_period.date() :]  # noqa

    serialized_output = df.to_json(
        orient="records", date_format="iso", double_precision=2
    )

    # i do this to get that beautiful serialization that pandas provides with date formatting and rounding
    # pandas is amazing, xoxo forever
    serialized_output = json.loads(serialized_output)

    response["logs"] = serialized_output

    return response


def get_overview_sleep_data(user, start_period, end_period):
    response = {
        "start_period": start_period.date().isoformat(),
        "end_period": end_period.date().isoformat(),
        "logs": [],
        "mean_start_time": None,
        "mean_end_time": None,
    }

    sleep_logs = SleepLog.objects.filter(
        user=user, start_time__lte=end_period, end_time__gte=start_period
    ).order_by("start_time")
    if not sleep_logs.exists():
        return response

    df = pd.DataFrame.from_records(sleep_logs.values("start_time", "end_time"))

    df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M").dt.time
    df["end_time"] = pd.to_datetime(df["end_time"], format="%H:%M").dt.time

    mean_start_time = mean_time(df["start_time"].values)
    mean_end_time = mean_time(df["end_time"].values)

    response["mean_start_time"] = mean_start_time
    response["mean_end_time"] = mean_end_time

    serializer = SleepLogReadSerializer(sleep_logs, many=True)
    sleep_logs_serialized = serializer.data
    response["logs"] = sleep_logs_serialized

    return response


class OverviewView(APIView):
    def get(self, request, period, date):
        user = request.user

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

        if period == "daily":
            end_period = start_period
        elif period == "weekly":
            end_period = get_time_relative_units_forward(start_period, weeks=1)
        elif period == "monthly":
            end_period = get_time_relative_units_forward(start_period, months=1)
        else:
            raise ValueError(f"Invalid Period {period}")

        # set the end to a datetime at 11:59 PM
        end_period = datetime(
            year=end_period.year,
            month=end_period.month,
            day=end_period.day,
            hour=23,
            minute=59,
            second=59,
            tzinfo=user.timezone,
        )

        sleep_data = get_overview_sleep_data(
            user, start_period=start_period, end_period=end_period
        )
        supplements_data = get_overview_supplements_data(
            user=user, start_period=start_period, end_period=end_period
        )

        productivity_data = get_overview_productivity_data(
            user=user, start_period=start_period, end_period=end_period
        )

        response = {
            "period": period,
            # change it back to date, so it doesn't look super confusing ...
            "start_period": start_period.date().isoformat(),
            "end_period": end_period.date().isoformat(),
            "sleep": sleep_data,
            "supplements": supplements_data,
            "productivity": productivity_data,
        }

        return Response(response)
