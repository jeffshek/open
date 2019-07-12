import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, UUIDField
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    uuid = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
