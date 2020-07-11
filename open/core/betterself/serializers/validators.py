from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from open.core.betterself.models.activity import Activity
from open.core.betterself.models.ingredient_composition import IngredientComposition


def ingredient_composition_uuid_validator(uuid):
    validate_model_uuid(IngredientComposition, uuid)
    return uuid


def validate_model_uuid(model, uuid, user=None):
    try:
        if user:
            model.objects.get(uuid=uuid, user=user)
        else:
            model.objects.get(uuid=uuid)

    except ObjectDoesNotExist:
        raise ValidationError(f"Cannot Find {model._meta.verbose_name.title()} UUID")


class ModelValidatorsMixin:
    """ a mixin holding all the commonly used validators in the validate_X step"""

    def validate_activity_uuid(self, value):
        user = None
        if self.context["request"]:
            user = self.context["request"].user

        validate_model_uuid(Activity, uuid=value, user=user)
        return value
