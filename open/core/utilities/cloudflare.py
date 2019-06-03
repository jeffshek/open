from django.conf import settings
import requests

# import pandas as pd


def get_dashboard_history():
    cloudflare_headers = {
        "X-Auth-Email": settings.CLOUDFLARE_EMAIL,
        "X-Auth-Key": settings.CLOUDFLARE_API_KEY,
    }

    cloudflare_prefix = "https://api.cloudflare.com/client/v4/zones"
    cf_url = (
        f"{cloudflare_prefix}/{settings.CLOUDFLARE_SENRIGAN_ZONE_ID}/analytics/dashboard?since=2019-05-01T12:23:00Z&until=2019-05-05T12:23:00Z&continuous=true"  # noqa: E501
    )

    response = requests.get(cf_url, headers=cloudflare_headers)

    data = response.json()
    return data
