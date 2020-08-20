"""

Reason : This was used to import a legacy app from heroku onto GCP (this was a connection to postgresql database)

I wrote this really quickly, so it probably could be refactored, but it's a one-time use file, so it's not as clean.
Sorta didn't realize how much data I had until I started writing this lol. 2017 version of you was very hard-working, just not very smart.

dpy runscript betterself_import_legacy_app
"""
from collections import defaultdict

import pandas as pd
from cachetools import cached
from django.conf import settings
from sqlalchemy import create_engine

from open.core.betterself.models.activity import Activity
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.models.supplement_stack_composition import (
    SupplementStackComposition,
)
from open.core.betterself.models.well_being_log import WellBeingLog
from open.users.models import User
from open.utilities.dataframes import change_dataframe_nans_to_none

"""
postgresql-sqlalchemy from https://gist.github.com/kunanit/eb0723eef653788395bb41c661c1fa86
"""
DATABASES = {
    "production": {
        "NAME": settings.BETTERSELF_LEGACY_DB_NAME,
        "USER": settings.BETTERSELF_LEGACY_DB_USER,
        "PASSWORD": settings.BETTERSELF_LEGACY_DB_PASSWORD,
        "HOST": settings.BETTERSELF_LEGACY_DB_HOST,
        "PORT": 5432,
    },
}

# choose the database to use
db = DATABASES["production"]

# construct an engine connection string
engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
    user=db["USER"],
    password=db["PASSWORD"],
    host=db["HOST"],
    port=db["PORT"],
    database=db["NAME"],
)

local_store = defaultdict(lambda: None)


def get_matching_row(df, column: str, matching_value):
    if column == "id":
        return df.loc[matching_value]

    result = df[column] == matching_value
    matched_df = df[result]

    assert len(matched_df) == 1
    return matched_df.iloc[0]


@cached(cache={})
def get_matching_user(legacy_id):
    engine = local_store["engine"]

    if local_store["users_df"] is None:
        users_df = pd.read_sql_table("users_user", engine, index_col="id")
        local_store["users_df"] = users_df
    else:
        users_df = local_store["users_df"]

    user_uuid = get_matching_row(users_df, "id", legacy_id)["uuid"]
    user = User.objects.get(uuid=user_uuid)
    return user


@cached(cache={})
def get_matching_activity(activity_id):
    engine = local_store["engine"]

    if local_store["events_useractivity"] is None:
        events_useractivity = pd.read_sql_table(
            "events_useractivity", engine, index_col="id"
        )
        local_store["events_useractivity"] = events_useractivity
    else:
        events_useractivity = local_store["events_useractivity"]

    # get the matching activity and then grab the uuid (what you've stored it locally as)
    activity_uuid = get_matching_row(events_useractivity, "id", activity_id)["uuid"]
    activity = Activity.objects.get(uuid=activity_uuid)

    return activity


@cached(cache={})
def get_matching_supplement(legacy_id):
    engine = local_store["engine"]

    if local_store["supplements_df"] is None:
        supplements_df = pd.read_sql_table(
            "supplements_supplement", engine, index_col="id"
        )
        local_store["supplements_df"] = supplements_df
    else:
        supplements_df = local_store["supplements_df"]

    instance_uuid = get_matching_row(supplements_df, "id", legacy_id)["uuid"]
    instance = Supplement.objects.get(uuid=instance_uuid)
    return instance


@cached(cache={})
def get_matching_supplement_stack(legacy_id):
    engine = local_store["engine"]

    if local_store["supplements_usersupplementstack"] is None:
        supplements_usersupplementstack = pd.read_sql_table(
            "supplements_supplement", engine, index_col="id"
        )
        local_store["supplements_usersupplementstack"] = supplements_usersupplementstack
    else:
        supplements_usersupplementstack = local_store["supplements_usersupplementstack"]

    instance_uuid = get_matching_row(supplements_usersupplementstack, "id", legacy_id)[
        "uuid"
    ]
    instance = SupplementStack.objects.get(uuid=instance_uuid)
    return instance


def import_legacy_users(engine):
    print("Importing Legacy Users")
    users_df = pd.read_sql_table("users_user", engine, index_col="id")
    # avoid recursively having to get this over and over
    local_store["users_df"] = users_df

    for index, legacy_user_details in users_df.iterrows():

        email = legacy_user_details["email"]
        username = legacy_user_details["username"]
        date_joined = (
            legacy_user_details["date_joined"]
            if not pd.isnull(legacy_user_details["date_joined"])
            else None
        )
        last_login = (
            legacy_user_details["last_login"]
            if not pd.isnull(legacy_user_details["last_login"])
            else None
        )

        defaults = {
            "password": legacy_user_details["password"],
            "last_login": last_login,
            "uuid": legacy_user_details["uuid"],  # i hope this part works
            "first_name": legacy_user_details["first_name"],
            "last_name": legacy_user_details["last_name"],
            "date_joined": date_joined,
            "name": legacy_user_details["name"],
            "timezone_string": legacy_user_details["timezone"],
            "is_betterself_user": True,
            "signed_up_from": "betterself",
        }

        updated_user, _ = User.objects.update_or_create(
            username=username, email=email, defaults=defaults
        )


def import_legacy_productivity(engine):
    print("Importing Productivity")

    productivity_df = pd.read_sql_table(
        "events_dailyproductivitylog", engine, index_col="id"
    )
    productivity_df = change_dataframe_nans_to_none(productivity_df)

    local_store["productivity_df"] = productivity_df

    attributes_to_import = [
        "uuid",
        "source",
        "date",
        "very_productive_time_minutes",
        "productive_time_minutes",
        "neutral_time_minutes",
        "distracting_time_minutes",
        "very_distracting_time_minutes",
    ]

    for index, details in productivity_df.iterrows():
        user = get_matching_user(details["user_id"])

        defaults = details[attributes_to_import].to_dict()
        defaults["source"] = "legacy_import"

        date = defaults.pop("date")
        productivity_log, _ = DailyProductivityLog.objects.update_or_create(
            user=user, date=date, defaults=defaults
        )


def import_legacy_sleep_log(engine):
    print("Importing Sleep")

    df = pd.read_sql_table("events_sleeplog", engine, index_col="id")
    df = change_dataframe_nans_to_none(df)

    attributes_to_import = [
        "uuid",
        "source",
        "start_time",
        "end_time",
        "modified",
    ]

    for index, details in df.iterrows():
        user = get_matching_user(details["user_id"])

        defaults = details[attributes_to_import].to_dict()
        defaults["source"] = "legacy_import"

        start_time = defaults.pop("start_time")
        end_time = defaults.pop("end_time")

        sleep_log, _ = SleepLog.objects.update_or_create(
            user=user, start_time=start_time, end_time=end_time, defaults=defaults
        )


def import_legacy_supplements(engine):
    print("Importing Supplements")

    df = pd.read_sql_table("supplements_supplement", engine, index_col="id")
    df = change_dataframe_nans_to_none(df)
    local_store["supplements_df"] = df

    attributes_to_import = [
        "uuid",
        "name",
        "modified",
    ]

    for index, details in df.iterrows():
        user = get_matching_user(details["user_id"])

        defaults = details[attributes_to_import].to_dict()

        name = defaults.pop("name")
        instance, _ = Supplement.objects.update_or_create(
            user=user, name=name, defaults=defaults
        )


def import_legacy_supplements_log(engine):
    print("Importing Supplements Log")

    df = pd.read_sql_table("events_supplementlog", engine, index_col="id")
    df = change_dataframe_nans_to_none(df)
    local_store["supplement_log_df"] = df
    print("Finished Importing Table from Heroku")

    last_dt = df["time"].max()

    # convoluted crap to deal with import was too slow, now handle via batch updates instead
    distinct_users = df["user_id"].unique()

    for user_id in distinct_users:
        user = get_matching_user(user_id)
        # wipe out the previous imports to do it one much larger operation, otherwise it
        # was taking too long on production
        SupplementLog.objects.filter(user=user, time__lte=last_dt).delete()

    attributes_to_import = [
        "modified",
        "uuid",
        "quantity",
        "duration_minutes",
        "notes",
    ]

    supplement_logs_to_create = []
    for index, details in df.iterrows():
        user = get_matching_user(details["user_id"])
        supplement = get_matching_supplement(details["supplement_id"])
        time = details["time"]

        defaults = details[attributes_to_import].to_dict()
        defaults["source"] = "legacy_import"

        instance = SupplementLog(
            user=user, supplement=supplement, time=time, **defaults
        )
        supplement_logs_to_create.append(instance)

        if index % 500 == 0:
            print(f"Adding {instance} to Supplement Logs to Create")

    print(f"Bulk Creating Supplements")
    SupplementLog.objects.bulk_create(supplement_logs_to_create, 500)
    print(f"Finished Creating Supplements")


def import_legacy_activities(engine):
    print("Importing Activities")

    df = pd.read_sql_table("events_useractivity", engine, index_col="id")
    df = change_dataframe_nans_to_none(df)
    local_store["activities_df"] = df

    print("Finished Importing Table from Heroku")

    activities_log_df = pd.read_sql_table(
        "events_useractivitylog", engine, index_col="id"
    )
    activities_log_df = change_dataframe_nans_to_none(activities_log_df)
    local_store["activities_log_df"] = df

    activities_used = activities_log_df["user_activity_id"].unique()

    # most activities you auto-created by default don't need to be used. don't import those
    activities_to_import = df.loc[activities_used]

    attributes_to_import = [
        "modified",
        "uuid",
        "name",
        "is_negative_activity",
        "is_all_day_activity",
    ]

    for index, details in activities_to_import.iterrows():
        user = get_matching_user(details["user_id"])

        defaults = details[attributes_to_import].to_dict()

        name = defaults.pop("name")

        instance, _ = Activity.objects.update_or_create(
            user=user, name=name, defaults=defaults
        )


def import_legacy_activities_logs(engine):
    print("Importing Activities Logs")

    df = pd.read_sql_table("events_useractivity", engine, index_col="id")
    df = change_dataframe_nans_to_none(df)
    local_store["activities_df"] = df

    print("Finished Importing Table from Heroku")

    activities_log_df = pd.read_sql_table(
        "events_useractivitylog", engine, index_col="id"
    )
    activities_log_df = change_dataframe_nans_to_none(activities_log_df)
    local_store["activities_log_df"] = df

    attributes_to_import = [
        "modified",
        "uuid",
        "source",
        "duration_minutes",
    ]

    for index, details in activities_log_df.iterrows():
        time = details["time"]

        user_id = details["user_id"]
        user = get_matching_user(user_id)

        activity_id = details["user_activity_id"]
        activity = get_matching_activity(activity_id)

        defaults = details[attributes_to_import].to_dict()
        defaults["source"] = "legacy_import"

        ActivityLog.objects.update_or_create(
            time=time, user=user, activity=activity, defaults=defaults
        )


def import_legacy_mood_logs(engine):
    print("Importing Mood Logs")

    df = pd.read_sql_table("events_usermoodlog", engine, index_col="id")
    df = change_dataframe_nans_to_none(df)
    local_store["mood_log"] = df

    attributes_to_import = [
        "modified",
        "uuid",
        "source",
        "notes",
    ]

    for index, details in df.iterrows():
        user = get_matching_user(details["user_id"])
        mental_value = details["value"]
        time = details["time"]

        defaults = details[attributes_to_import].to_dict()
        defaults["source"] = "legacy_import"

        instance, _ = WellBeingLog.objects.update_or_create(
            user=user, time=time, mental_value=mental_value, defaults=defaults
        )


def import_supplement_stack_and_compositions(engine):
    print("Importing Supplement Stacks")

    supplements_usersupplementstack = pd.read_sql_table(
        "supplements_usersupplementstack", engine, index_col="id"
    )
    supplements_usersupplementstack = change_dataframe_nans_to_none(
        supplements_usersupplementstack
    )
    local_store["supplements_usersupplementstack"] = supplements_usersupplementstack

    attributes_to_import = [
        "modified",
        "uuid",
    ]

    for index, details in supplements_usersupplementstack.iterrows():
        user = get_matching_user(details["user_id"])
        name = details["name"]

        defaults = details[attributes_to_import].to_dict()

        SupplementStack.objects.update_or_create(
            user=user, name=name, defaults=defaults
        )

    # okay, now that all the stacks have been imported ... let's add the actual compositions
    supplements_usersupplementstackcomposition = pd.read_sql_table(
        "supplements_usersupplementstackcomposition", engine, index_col="id"
    )
    supplements_usersupplementstackcomposition = change_dataframe_nans_to_none(
        supplements_usersupplementstackcomposition
    )
    local_store[
        "supplements_usersupplementstackcomposition"
    ] = supplements_usersupplementstackcomposition

    attributes_to_import = [
        "modified",
        "uuid",
        "quantity",
    ]

    for index, details in supplements_usersupplementstackcomposition.iterrows():
        user = get_matching_user(details["user_id"])
        supplement = get_matching_supplement(details["supplement_id"])
        supplement_stack = get_matching_supplement_stack(details["stack_id"])

        # omfg, this is so clean. love pandas
        defaults = details[attributes_to_import].to_dict()

        SupplementStackComposition.objects.update_or_create(
            user=user, supplement=supplement, stack=supplement_stack, defaults=defaults
        )


def run_():
    engine = create_engine(engine_string)
    local_store["engine"] = engine
    #
    # import_legacy_users(engine)
    # import_legacy_productivity(engine)
    # import_legacy_sleep_log(engine)
    # import_legacy_supplements(engine)
    # import_legacy_supplements_log(engine)
    import_legacy_activities(engine)
    import_legacy_activities_logs(engine)
    import_legacy_mood_logs(engine)
    import_supplement_stack_and_compositions(engine)


def run():
    run_()
