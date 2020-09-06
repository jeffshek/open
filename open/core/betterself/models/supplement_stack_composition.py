from django.db.models import DecimalField, ForeignKey, CASCADE

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_stack import SupplementStack
from open.utilities.models import BaseModelWithUserGeneratedContent


class SupplementStackComposition(BaseModelWithUserGeneratedContent):
    RESOURCE_NAME = BetterSelfResourceConstants.SUPPLEMENT_STACK_COMPOSITIONS

    supplement = ForeignKey(Supplement, on_delete=CASCADE)
    stack = ForeignKey(SupplementStack, related_name="compositions", on_delete=CASCADE)
    # by default, don't allow this to be blank, it doesn't make sense for a supplement stack
    quantity = DecimalField(
        max_digits=10, decimal_places=4, null=False, blank=False, default=1
    )

    class Meta:
        unique_together = ("user", "supplement", "stack")
        verbose_name = "Supplement Stack Composition"

    def __str__(self):
        return "{}-{}".format(self.stack_id, self.supplement_id)

    @property
    def description(self):
        return "{quantity} {supplement}".format(
            quantity=self.quantity, supplement=self.supplement
        )
