from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from open.core.betterself.models.activity import Activity
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.models.supplement import Supplement
from functools import partial


def ingredient_composition_uuid_validator(uuid):
    validate_model_uuid(uuid, IngredientComposition)
    return uuid


def supplement_uuid_validator(uuid):
    validate_model_uuid(uuid, Supplement)
    return uuid


def generic_model_uuid_validator(model):
    return partial(validate_model_uuid, model=model)


def validate_model_uuid(uuid, model, user=None):
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

        validate_model_uuid(uuid=value, model=Activity, user=user)
        return value
