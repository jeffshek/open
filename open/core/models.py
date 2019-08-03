from django.db.models import TextField

from open.utilities.models import BaseModel


class WriteUpSharedPrompt(BaseModel):
    text = TextField(default="", blank=True)
    email = TextField(default="", blank=True)
    title = TextField(default="", blank=True)
