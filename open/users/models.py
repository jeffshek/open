import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, UUIDField, BooleanField, DateTimeField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoLastModifiedField
from rest_framework.authtoken.models import Token

from open.constants import SIGNED_UP_FROM_DETAILS_CHOICE

import pytz

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    uuid = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)

    # used to determine where a user signed up from
    signed_up_from = CharField(
        choices=SIGNED_UP_FROM_DETAILS_CHOICE, default="", blank=True, max_length=255
    )

    # for specific features that are specific to an app
    is_writeup_user = BooleanField(default=False)
    is_betterself_user = BooleanField(default=False)

    # doing this lets you insert records and modify the timestamps of created
    created = DateTimeField(default=timezone.now, editable=False, blank=True)
    modified = AutoLastModifiedField(_("modified"))

    # have it stored as a string here, then use a property to grab the timezones
    timezone_string = CharField(max_length=32, choices=TIMEZONES, default="US/Eastern")

    class Meta:
        ordering = ["-id"]

    @property
    def timezone(self):
        return pytz.timezone(self.timezone_string)

    def save(self, *args, **kwargs):
        needs_api_key = False
        if not self.pk:
            needs_api_key = True

        super().save(*args, **kwargs)

        if needs_api_key:
            Token.objects.get_or_create(user=self)
