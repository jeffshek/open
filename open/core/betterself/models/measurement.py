from django.db.models import BooleanField, CharField

from open.utilities.models import BaseModel


class Measurement(BaseModel):
    name = CharField(max_length=100, unique=True)  # 'milligram'
    short_name = CharField(max_length=100, default="", blank=True)  # 'ml'
    is_liquid = BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
