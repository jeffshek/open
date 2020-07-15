import uuid

from django.db.models import DateTimeField, UUIDField, ForeignKey, CASCADE, TextField
from django.utils import timezone
from model_utils.models import TimeStampedModel
from rest_framework.reverse import reverse

from open.users.models import User


class BaseModel(TimeStampedModel):
    # doing this lets you insert records and modify the timestamps of created
    created = DateTimeField(default=timezone.now, editable=False, blank=True)
    uuid = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)

    # modified is inherited from TimeStampedModel

    class Meta:
        abstract = True

    @property
    def uuid_str(self):
        # i frequently get the str of uuid a lot
        return self.uuid.__str__()


class BaseModelWithUserGeneratedContent(BaseModel):
    user = ForeignKey(User, null=False, blank=False, on_delete=CASCADE)
    notes = TextField(default="")

    class Meta:
        abstract = True

    def get_update_url(self):
        instance_uuid = str(self.uuid)
        kwargs = {"uuid": instance_uuid}
        update_url = reverse(self.RESOURCE_NAME, kwargs=kwargs)
        return update_url

    def __repr__(self):
        has_name_attr = getattr(self, "name", "")
        if has_name_attr:
            label = f"ID {self.id} | {self._meta.verbose_name.title()} - {self.name}"
        else:
            label = f"ID {self.id} | {self._meta.verbose_name.title()}"

        return label

    def __str__(self):
        return self.__repr__()
