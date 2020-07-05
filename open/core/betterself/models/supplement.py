from django.db.models import CharField, ManyToManyField, TextField

from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.utilities.models import BaseModelWithUserGeneratedContent


class Supplement(BaseModelWithUserGeneratedContent):
    """
    Could be a stack like BCAA (which would have 4 ingredient comps)
    Or could just be something simple like Caffeine.
    """

    name = CharField(max_length=300)
    ingredient_compositions = ManyToManyField(IngredientComposition, blank=True)
    notes = TextField(default="")

    # quantity is an event type of attribute, so its not here.

    class Meta:
        unique_together = ("user", "name")
        ordering = ["user", "name"]
        verbose_name = "Supplement"
        verbose_name_plural = "Supplements"
