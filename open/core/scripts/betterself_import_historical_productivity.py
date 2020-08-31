# a file for you to import your legacy productivity files
from datetime import date as datetime_date

import requests
from django.conf import settings
import pandas as pd

"""
dpy runscript betterself_import_historical_productivity
"""


def run():
    url = "https://open.senrigan.io/api/betterself/v2/productivity_logs/"

    df = pd.read_excel(
        "snapshots/personal_historical_pomodoros.xlsx", keep_default_na=""
    )
    token_key = f"Token {settings.BETTERSELF_PERSONAL_API_KEY}"
    headers = {"Authorization": token_key}

    df.index = df["Date"]
    df = df.sort_index()

    start_import_period = datetime_date(2020, 7, 9)
    end_import_period = datetime_date(2020, 7, 28)

    for index, row in df.iterrows():
        date = row["Date"].date().isoformat()

        should_import = start_import_period <= index.date() <= end_import_period
        if not should_import:
            continue

        notes = row["Description Of Day"]
        mistakes = row["Mistakes"]
        pomodoro_count = row["Pomodoros"]

        if not pomodoro_count:
            continue

        data = {
            "pomodoro_count": pomodoro_count,
            "date": date,
            "notes": notes,
            "mistakes": mistakes,
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            print(response.content)
            assert response.status_code == 200
