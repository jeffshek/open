# flake8: noqa
import binascii
import logging
import os

from django.db import migrations

from open.users.utilities import create_user_api_tokens

logger = logging.getLogger()


def load_data(apps, schema_editor):
    User = apps.get_model("users", "User")
    users = User.objects.all()

    Token = apps.get_model("authtoken", "Token")
    Token.objects.all().delete()

    for user in users:
        key = binascii.hexlify(os.urandom(20)).decode()
        Token.objects.get_or_create(user=user, key=key)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_auto_20200711_2029"),
    ]

    operations = [migrations.RunPython(load_data)]
