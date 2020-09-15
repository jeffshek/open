from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.betterself.utilities.history_overview_utilities import (
    get_overview_supplements_data,
    get_overview_productivity_data,
    get_overview_sleep_data,
)
from open.core.betterself.utilities.user_date_utilities import (
    serialize_date_to_user_localized_datetime,
    serialize_end_date_to_user_localized_datetime,
)


class OverviewView(APIView):
    def get(self, request, start_date, end_date):
        user = request.user
        start_period = serialize_date_to_user_localized_datetime(start_date, user)
        end_period = serialize_end_date_to_user_localized_datetime(end_date, user)

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
            # change it back to date, so it doesn't look super confusing on api response ...
            "start_period": start_period.date().isoformat(),
            "end_period": end_period.date().isoformat(),
            "sleep": sleep_data,
            "supplements": supplements_data,
            "productivity": productivity_data,
        }

        return Response(response)
