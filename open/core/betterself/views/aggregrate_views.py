from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.betterself.models.supplement import Supplement
from open.core.betterself.serializers.aggregrate_serializers import (
    AggregrateViewParamsSerializer,
)
from open.core.betterself.utilities.history_overview_utilities import (
    get_overview_supplements_data,
)
from open.core.betterself.utilities.user_date_utilities import (
    serialize_date_to_user_localized_datetime,
    serialize_end_date_to_user_localized_datetime,
)


class AggregateView(APIView):
    """
    Only working for Supplements for now, I'll add more when it makes sense to
    - This should eventually support food / activities too
    """

    def post(self, request):
        user = request.user

        serializer = AggregrateViewParamsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # convert to start (00:00) and end of day (23:59)
        start_period = serialize_date_to_user_localized_datetime(
            data["start_date"], user
        )
        end_period = serialize_end_date_to_user_localized_datetime(
            data["end_date"], user
        )

        response = {
            # change it back to date, so it doesn't look super confusing on api response ...
            "start_period": start_period.date().isoformat(),
            "end_period": end_period.date().isoformat(),
        }

        supplement_uuids = data.get("supplement_uuids")
        if supplement_uuids:
            supplements = Supplement.objects.filter(uuid__in=supplement_uuids)
            supplements_data = get_overview_supplements_data(
                user=user,
                start_period=start_period,
                end_period=end_period,
                supplements=supplements,
            )
            response["supplements"] = supplements_data

        # productivity_data = get_overview_productivity_data(
        #     user=user, start_period=start_period, end_period=end_period
        # )

        return Response(response)
