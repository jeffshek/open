import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, UUIDField, BooleanField
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from open.constants import SIGNED_UP_FROM_DETAILS_CHOICE


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

    def save(self, *args, **kwargs):
        needs_api_key = False
        if not self.pk:
            needs_api_key = True

        super().save(*args, **kwargs)

        if needs_api_key:
            Token.objects.get_or_create(user=self)
