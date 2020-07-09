from django.db.models import PositiveIntegerField, CharField

from open.core.betterself.constants import BetterSelfResourceConstants
from open.utilities.models import BaseModelWithUserGeneratedContent


class Ingredient(BaseModelWithUserGeneratedContent):
    RESOURCE_NAME = BetterSelfResourceConstants.INGREDIENTS

    # if some ingredient is longer than 300 characters, prob shouldn't take it.
    # if anyone ever reads up reading this, 1,3 dimethylamylamine is probably a great
    # example of if you can't pronounce it, don't take it.
    name = CharField(max_length=255, default="", blank=False, null=False)
    # name = TextField(default="", blank=False, null=False)
    # this is going to be a hard thing to source / scrap, but you do care about this, leave blank
    # but don't let default be zero.
    half_life_minutes = PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Ingredient | {self.name} - {self.user}"

    class Meta:
        unique_together = ("name", "user")
