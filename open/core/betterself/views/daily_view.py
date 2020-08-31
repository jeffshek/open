from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.betterself.utilities.user_date_utilities import (
    serialize_date_to_user_localized_date,
)
from open.core.betterself.utilities.history_overview_utilities import (
    get_overview_supplements_data,
    get_overview_productivity_data,
    get_overview_sleep_data,
    get_overview_well_being_data,
    get_overview_activity_data,
    get_overview_food_data,
)


class DailyReviewView(APIView):
    def get(self, request, date):
        user = request.user
        start_period = serialize_date_to_user_localized_date(date, user)

        # use the start_period, but now get the end of the day
        end_period = datetime(
            year=start_period.year,
            month=start_period.month,
            day=start_period.day,
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

        well_being_data = get_overview_well_being_data(
            user=user, start_period=start_period, end_period=end_period
        )
        activities_data = get_overview_activity_data(
            user=user, start_period=start_period, end_period=end_period
        )
        foods_data = get_overview_food_data(
            user=user, start_period=start_period, end_period=end_period
        )

        response = {
            # change it back to a date, so it doesn't look super confusing on api response ...
            "date": start_period.date().isoformat(),
            "activities": activities_data,
            "foods": foods_data,
            "productivity": productivity_data,
            "sleep": sleep_data,
            "supplements": supplements_data,
            "well_being_data": well_being_data,
        }

        return Response(response)
