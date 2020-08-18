"""
From: Styled / copied from https://gist.github.com/kunanit/eb0723eef653788395bb41c661c1fa86
Reason : This was used to import a legacy app from heroku onto GCP (this was a connection to postgresql database)

Steps To Run
--
pip install SQLAlchemy
dpy runscript betterself_import_legacy_app
"""
import ipdb
from ipdb import launch_ipdb_on_exception
from sqlalchemy import create_engine
from django.conf import settings
import pandas as pd

from open.users.models import User

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


def get_matching_row(df, column: str, matching_value):
    result = df[column] == matching_value
    matched_df = df[result]

    assert len(matched_df) == 1
    return matched_df.iloc[0]


def import_legacy_users():
    engine = create_engine(engine_string)
    users_df = pd.read_sql_table("users_user", engine, index_col="id")

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


def run_():
    import_legacy_users()


def run():
    with launch_ipdb_on_exception():
        run_()
