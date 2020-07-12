# flake8: noqa

import logging

from django.db import migrations

from open.users.utilities import create_user_api_tokens

logger = logging.getLogger()

"""
This file is a hack and technically a bad practice ...
"""


def load_data(apps, schema_editor):
    create_user_api_tokens()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_auto_20200711_2029"),
    ]

    operations = [migrations.RunPython(load_data)]
