from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import datetime

from open.utilities.date_and_time import get_time_relative_units_forward

datetime.strptime("2014-12-04", "%Y-%m-%d").date()


class OverviewView(APIView):
    def get(self, request, period, date):
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise Http404

        start_period = date
        if period == "daily":
            end_period = start_period
        elif period == "weekly":
            end_period = get_time_relative_units_forward(start_period, weeks=7)
        elif period == "monthly":
            end_period = get_time_relative_units_forward(start_period, months=1)

        response = {
            "period": period,
            "start_period": start_period.isoformat(),
            "end_period": start_period.isoformat(),
        }

        return Response(response)
