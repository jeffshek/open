# flake8: noqa

import logging

from django.db import migrations

logger = logging.getLogger()


def load_data(apps, schema_editor):
    User = apps.get_model("users", "User")

    # don't worry, i changed the password after the datamigration
    user, _ = User.objects.get_or_create(
        username="demo-testing@senrigan.io",
        password="demo-testing@senrigan.io",
        email="demo-testing@senrigan.io",
    )
    label = f"Created {user}"
    print(label)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_add_measurement_name_uniqueness"),
    ]

    operations = [migrations.RunPython(load_data)]
