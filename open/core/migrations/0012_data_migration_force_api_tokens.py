# flake8: noqa

import logging

from django.db import migrations

from open.users.utilities import create_user_api_tokens

logger = logging.getLogger()


def load_data(apps, schema_editor):
    User = apps.get_model("users", "User")
    users = User.objects.all()

    Token = apps.get_model("authtoken", "Token")
    for user in users:
        Token.objects.get_or_create(user=user)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_auto_20200711_2029"),
    ]

    operations = [migrations.RunPython(load_data)]
