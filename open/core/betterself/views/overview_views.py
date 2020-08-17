from datetime import datetime

import pandas as pd
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.serializers.sleep_log_serializers import (
    SleepLogReadSerializer,
)
from open.utilities.date_and_time import get_time_relative_units_forward, mean_time


def get_supplements_overview(user, start_period, end_period):
    return


def get_sleep_overview_response(user, start_period, end_period):
    response = {
        "start_period": start_period.date().isoformat(),
        "end_period": end_period.date().isoformat(),
        "logs": [],
        "mean_start_time": None,
        "mean_end_time": None,
    }

    sleep_logs = SleepLog.objects.filter(
        user=user, start_time__lte=end_period, end_time__gte=start_period
    )
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
            end_period = get_time_relative_units_forward(start_period, weeks=7)
        elif period == "monthly":
            end_period = get_time_relative_units_forward(start_period, months=1)

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

        sleep_data = get_sleep_overview_response(
            user, start_period=start_period, end_period=end_period
        )

        response = {
            "period": period,
            # change it back to date, so it doesn't look super confusing ...
            "start_period": start_period.date().isoformat(),
            "end_period": end_period.date().isoformat(),
            "sleep_data": sleep_data,
        }

        return Response(response)
