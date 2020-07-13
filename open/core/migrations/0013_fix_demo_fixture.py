# flake8: noqa

import logging

from django.contrib.auth.hashers import make_password
from django.db import migrations

from open.core.betterself.constants import DEMO_TESTING_ACCOUNT

logger = logging.getLogger()


def load_data(apps, schema_editor):
    User = apps.get_model("users", "User")
    adjusted_password = make_password(DEMO_TESTING_ACCOUNT)

    demo_user, _ = User.objects.get_or_create(username=DEMO_TESTING_ACCOUNT)
    demo_user.password = adjusted_password
    demo_user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_data_migration_force_api_tokens"),
    ]

    operations = [migrations.RunPython(load_data)]
