from django.db.models import ForeignKey, DecimalField, CASCADE

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.measurement import Measurement
from open.utilities.models import BaseModelWithUserGeneratedContent


class IngredientComposition(BaseModelWithUserGeneratedContent):
    """ Creatine, 5, grams """

    RESOURCE_NAME = BetterSelfResourceConstants.INGREDIENT_COMPOSITIONS

    ingredient = ForeignKey(Ingredient, on_delete=CASCADE)
    # users should fill this in if they want to use a composition ... otherwise, they could
    # just leave it at supplement
    measurement = ForeignKey(Measurement, null=False, blank=False, on_delete=CASCADE)
    quantity = DecimalField(max_digits=10, decimal_places=4, null=False, blank=True)

    class Meta:
        unique_together = ("user", "ingredient", "measurement", "quantity")
        ordering = ["user", "ingredient__name"]
        verbose_name = "Ingredient Composition"
        verbose_name_plural = "Ingredient Compositions"

    def __str__(self):
        return f"IngredientComposition | {self.ingredient.name} {self.quantity} {self.measurement.name}"
