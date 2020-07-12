# flake8: noqa

import logging

from django.contrib.auth.hashers import make_password
from django.db import migrations

from open.core.betterself.constants import DEMO_TESTING_ACCOUNT

logger = logging.getLogger()


def load_data(apps, schema_editor):
    User = apps.get_model("users", "User")

    # don't worry, i changed the password after the datamigration!
    adjusted_password = make_password(DEMO_TESTING_ACCOUNT)

    user, _ = User.objects.get_or_create(
        username=DEMO_TESTING_ACCOUNT,
        password=adjusted_password,
        email=DEMO_TESTING_ACCOUNT,
    )
    # label = f"Created {user}"


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_add_measurement_name_uniqueness"),
    ]

    operations = [migrations.RunPython(load_data)]
