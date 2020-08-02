from django.db.models import (
    ForeignKey,
    DecimalField,
    CASCADE,
    CharField,
    DateTimeField,
)

from open.core.betterself.constants import (
    WEB_INPUT_SOURCE,
    INPUT_SOURCES_TUPLES,
    BetterSelfResourceConstants,
)
from open.core.betterself.models.food import Food
from open.utilities.models import BaseModelWithUserGeneratedContent


class FoodLog(BaseModelWithUserGeneratedContent):
    RESOURCE_NAME = BetterSelfResourceConstants.FOOD_LOGS

    food = ForeignKey(Food, on_delete=CASCADE)
    source = CharField(
        max_length=50, choices=INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE
    )
    quantity = DecimalField(max_digits=10, decimal_places=2, default=1)
    time = DateTimeField()

    class Meta:
        unique_together = ("user", "time", "food")
        ordering = ["user", "-time"]
        verbose_name = "Food Log"
        verbose_name_plural = "Food Logs"

    def __str__(self):
        formatted_time = self.time.strftime("%Y-%m-%d %I:%M%p")
        return f"{self.quantity:.0f} {self.food.name} {formatted_time} from {self.source} event"
