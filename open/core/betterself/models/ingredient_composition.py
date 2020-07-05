from django.db.models import ForeignKey, DecimalField, CASCADE

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.measurement import Measurement
from open.utilities.models import BaseModelWithUserGeneratedContent


class IngredientComposition(BaseModelWithUserGeneratedContent):
    """ Creatine, 5, grams """

    ingredient = ForeignKey(Ingredient, on_delete=CASCADE)

    # if someone doesn't really want to fill it in, it's okay to just have the ingredient and no measurements
    measurement = ForeignKey(Measurement, null=True, blank=True, on_delete=CASCADE)
    quantity = DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    class Meta:
        unique_together = ("user", "ingredient", "measurement", "quantity")
        ordering = ["user", "ingredient__name"]
        verbose_name = "Ingredient Composition"
        verbose_name_plural = "Ingredient Compositions"

    def __str__(self):
        if self.measurement:
            return "{ingredient.name} ({obj.quantity} {measurement.name})".format(
                obj=self, ingredient=self.ingredient, measurement=self.measurement
            )
        elif self.quantity != 1:
            return "{ingredient.name} ({obj.quantity})".format(
                obj=self, ingredient=self.ingredient
            )
        else:
            return "{ingredient.name}".format(ingredient=self.ingredient)

    def __repr__(self):
        return f"Ingredient Composition {self.id}"
