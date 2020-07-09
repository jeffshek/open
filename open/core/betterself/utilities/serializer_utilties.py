from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


def validate_model_uuid(model, uuid, user=None):
    try:
        if user:
            model.objects.get(uuid=uuid, user=user)
        else:
            model.objects.get(uuid=uuid)

    except ObjectDoesNotExist:
        raise ValidationError(f"Cannot Find {model._meta.verbose_name.title()} UUID")
