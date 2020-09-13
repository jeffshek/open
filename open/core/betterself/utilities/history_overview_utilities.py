import json
from collections import defaultdict
from datetime import datetime

import dateutil.parser
import pandas as pd
from django.db.models import Sum

from open.core.betterself.constants import PRODUCTIVITY_METRICS
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.models.food_logs import FoodLog
from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.models.well_being_log import WellBeingLog
from open.core.betterself.serializers.activity_log_serializers import (
    ActivityLogReadSerializer,
)
from open.core.betterself.serializers.food_log_serializers import FoodLogReadSerializer
from open.core.betterself.serializers.sleep_log_serializers import (
    SleepLogReadSerializer,
)
from open.core.betterself.serializers.supplement_log_serializers import (
    SupplementLogReadSerializer,
)
from open.core.betterself.serializers.supplement_serializers import (
    SimpleSupplementReadSerializer,
)
from open.core.betterself.serializers.well_being_log_serializers import (
    WellBeingLogReadSerializer,
)
from open.utilities.date_and_time import (
    get_time_relative_units_ago,
    yyyy_mm_dd_format_1,
    mean_time,
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

SUPPLEMENT_LOG_TYPE = "Supplement"
PRODUCTIVITY_LOG_TYPE = "Productivity"
SLEEP_LOG_TYPE = "Sleep"
WELL_BEING_LOG_TYPE = "Well Being"
ACTIVITY_LOG_TYPE = "Activity"
FOOD_LOG_TYPE = "Food"


def get_overview_supplements_data(
    user, start_period, end_period, filter_supplements=None
):
    response = {
        "start_period": start_period.date().isoformat(),
        "end_period": end_period.date().isoformat(),
        # group across each day and what supplements were taken
        # hence, this will be called "daily" logs
        "daily_logs": defaultdict(list),
        "logs": [],
        # group by supplements and how many were taken
        # currently using summary for supplements history overview
        "summary": [],
        "total_quantity": 0,
        "log_type": SUPPLEMENT_LOG_TYPE,
    }

    supplement_logs = (
        SupplementLog.objects.filter(
            user=user, time__lte=end_period, time__gte=start_period
        )
        .select_related("supplement")
        .order_by("time")
    )
    if not supplement_logs.exists():
        return response

    if filter_supplements:
        supplement_logs = supplement_logs.filter(supplement__in=filter_supplements)

    supplement_name_cache = {}

    for log in supplement_logs:
        # otherwise everything is stored on the UTC date for the user, which doesn't make as much sense
        user_timezone = user.timezone
        normalized_time = user_timezone.normalize(log.time)
        log_date = normalized_time.date().isoformat()
        supplement = log.supplement

        # serialize this data once to avoid duplicate SQL queries
        if supplement.uuid not in supplement_name_cache:
            supplement_name_cache[supplement.name] = SimpleSupplementReadSerializer(
                supplement
            ).data

        serialized_log = SupplementLogReadSerializer(log).data

        response["logs"].append(serialized_log)
        # haven't quite figured out what my ideal data structure is yet
        response["daily_logs"][log_date].append(serialized_log)

    # aggregate all the supplement logs, sort them by the name, and then count how many were used
    taken_data = (
        supplement_logs.values("supplement__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by()
    )

    for value in taken_data:
        taken_result = {}

        supplement_serialized = supplement_name_cache[value["supplement__name"]]
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
        "log_type": PRODUCTIVITY_LOG_TYPE,
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
        "start_time_mean": None,
        "end_time_mean": None,
        "total_duration_minutes": None,
        "total_duration_hours": None,
        "log_type": SLEEP_LOG_TYPE,
    }

    sleep_logs = SleepLog.objects.filter(
        user=user, start_time__lte=end_period, end_time__gte=start_period
    ).order_by("start_time")
    if not sleep_logs.exists():
        return response

    df = pd.DataFrame.from_records(sleep_logs.values("start_time", "end_time"))

    df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M").dt.time
    df["end_time"] = pd.to_datetime(df["end_time"], format="%H:%M").dt.time

    start_time_mean = mean_time(df["start_time"].values)
    end_time_mean = mean_time(df["end_time"].values)

    response["start_time_mean"] = start_time_mean
    response["end_time_mean"] = end_time_mean

    serializer = SleepLogReadSerializer(sleep_logs, many=True)
    sleep_logs_serialized = serializer.data

    time_slept_minutes = sum(
        [item["duration_minutes"] for item in sleep_logs_serialized]
    )
    time_slept_hours = time_slept_minutes / 60

    response["total_duration_minutes"] = time_slept_minutes
    response["total_duration_hours"] = time_slept_hours

    response["logs"] = sleep_logs_serialized

    return response


def get_overview_well_being_data(user, start_period, end_period):
    response = {
        "start_period": start_period.date().isoformat(),
        "end_period": end_period.date().isoformat(),
        "logs": [],
        "log_type": WELL_BEING_LOG_TYPE,
    }

    logs = WellBeingLog.objects.filter(
        user=user, time__lte=end_period, time__gte=start_period
    ).order_by("time")
    if not logs.exists():
        return response

    response["logs"] = WellBeingLogReadSerializer(logs, many=True).data
    return response


def get_overview_activity_data(user, start_period, end_period):
    response = {
        "start_period": start_period.date().isoformat(),
        "end_period": end_period.date().isoformat(),
        "logs": [],
        "log_type": ACTIVITY_LOG_TYPE,
    }

    logs = (
        ActivityLog.objects.filter(
            user=user, time__lte=end_period, time__gte=start_period
        )
        .order_by("time")
        .select_related("activity")
    )
    if not logs.exists():
        return response

    response["logs"] = ActivityLogReadSerializer(logs, many=True).data
    return response


def get_overview_food_data(user, start_period, end_period, filter_foods=None):
    response = {
        "start_period": start_period.date().isoformat(),
        "end_period": end_period.date().isoformat(),
        "daily_logs": defaultdict(list),
        "logs": [],
        "log_type": FOOD_LOG_TYPE,
    }

    logs = (
        FoodLog.objects.filter(user=user, time__lte=end_period, time__gte=start_period)
        .order_by("time")
        .select_related("food")
    )
    if not logs.exists():
        return response

    if filter_foods:
        logs = logs.filter(food__in=filter_foods)

    for log in logs:
        user_timezone = user.timezone
        normalized_time = user_timezone.normalize(log.time)
        log_date = normalized_time.date().isoformat()

        serialized_log = FoodLogReadSerializer(log).data
        response["logs"].append(serialized_log)
        response["daily_logs"][log_date].append(serialized_log)

    return response


def build_timeline_item(time, log_type, summary):
    result = {"time": time, "log_type": log_type, "summary": summary}
    return result


def get_timeline_data(
    sleep_data,
    supplements_data,
    productivity_data,
    well_being_data,
    activities_data,
    foods_data,
):
    response = []

    if sleep_data["logs"]:
        for sleep_log in sleep_data["logs"]:
            sleep_log_type = sleep_data["log_type"]

            sleep_start_item = {
                "time": sleep_log["start_time"],
                "log_type": sleep_log_type,
                "summary": "Went To Sleep",
            }
            sleep_end_time = {
                "time": sleep_log["end_time"],
                "log_type": sleep_log_type,
                "summary": "Woke Up!",
            }

            response.extend([sleep_start_item, sleep_end_time])

    logs_with_time_attributes = [
        supplements_data,
        well_being_data,
        activities_data,
        foods_data,
    ]
    for data in logs_with_time_attributes:
        logs = data["logs"]
        if not logs:
            continue

        log_type = data["log_type"]

        for log in logs:
            summary = ""
            if log_type == SUPPLEMENT_LOG_TYPE:
                summary = f"Took {log['quantity']} of {log['supplement']['name']}"
            elif log_type == WELL_BEING_LOG_TYPE:
                if log["mental_value"]:
                    summary += f"Mental Score: {log['mental_value']}\n"
                if log["physical_value"]:
                    summary += f"Physical Score: {log['physical_value']}\n"
                if log["notes"]:
                    summary += f"Notes: {log['notes']}"
            elif log_type == ACTIVITY_LOG_TYPE:
                summary = f"Did {log['activity']['name']}."
            elif log_type == FOOD_LOG_TYPE:
                summary = f"Ate {log['food']['name']}."

            timeline_item = {
                "time": log["time"],
                "log_type": log_type,
                "summary": summary,
            }
            response.append(timeline_item)

    response.sort(key=lambda x: dateutil.parser.parse(x["time"]))
    return response
