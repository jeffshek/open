from django.db.models import DateTimeField, UUIDField
from django.utils import timezone
from model_utils.models import TimeStampedModel
import uuid


class BaseModel(TimeStampedModel):
    # doing this lets you insert records and modify them
    created = DateTimeField(default=timezone.now, editable=False, blank=True)
    uuid = UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    @property
    def uuid_str(self):
        # i frequently get the str of uuid a lot
        return self.uuid.__str__()
