import pandas as pd
import requests
from django.conf import settings

start_date_default = "2019-05-04T00:00:00Z"
end_date_default = "2019-05-11T00:00:00Z"

CLOUDFLARE_HEADERS = {
    "X-Auth-Email": settings.CLOUDFLARE_EMAIL,
    "X-Auth-Key": settings.CLOUDFLARE_API_KEY,
}

CLOUDFLARE_PREFIX = "https://api.cloudflare.com/client/v4/zones"


def get_dashboard_history(start_date=start_date_default, end_date=end_date_default):
    cf_url = (
        f"{CLOUDFLARE_PREFIX}/{settings.CLOUDFLARE_SENRIGAN_ZONE_ID}/analytics/dashboard?since={start_date}&until={end_date}&"  # noqa: E501
    )
    response = requests.get(cf_url, headers=CLOUDFLARE_HEADERS)

    data = response.json()

    unique_values = []
    unique_dates = []

    timeseries = data["result"]["timeseries"]
    for daily_snapshot in timeseries:

        date_start = daily_snapshot["since"]
        uniques = daily_snapshot["uniques"]

        uniques_all = uniques["all"]

        # create two lists holding the dates and values to load into a pd.Series
        unique_dates.append(date_start)
        unique_values.append(uniques_all)

    series = pd.Series(data=unique_values, index=unique_dates)
    series.to_excel("exports/cloudflare_export_may.xlsx")

    return series
