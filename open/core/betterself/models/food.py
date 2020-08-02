from django.db.models import CharField, DecimalField, BooleanField

from open.core.betterself.constants import BetterSelfResourceConstants
from open.utilities.models import BaseModelWithUserGeneratedContent


class Food(BaseModelWithUserGeneratedContent):
    """
    Chips, candy and steak.
    """

    RESOURCE_NAME = BetterSelfResourceConstants.FOODS

    name = CharField(max_length=300)
    calories = DecimalField(max_digits=10, decimal_places=2, null=True)
    is_liquid = BooleanField(default=False)

    class Meta:
        unique_together = ("user", "name")
        ordering = ["user", "name"]
        verbose_name = "Food"
        verbose_name_plural = "Foods"
