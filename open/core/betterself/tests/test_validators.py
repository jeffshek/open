from rest_framework.exceptions import ValidationError
from test_plus import TestCase

from open.core.betterself.factories import SupplementFactory
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.serializers.validators import generic_model_uuid_validator
import uuid

"""
dpy test open.core.betterself.tests.test_validators --keepdb
"""


class TestValidators(TestCase):
    def test_partial_validator_with_supplement_uuid(self):
        supplement = SupplementFactory()
        supplement_uuid = str(supplement.uuid)

        validator = generic_model_uuid_validator(Supplement)

        result = validator(supplement_uuid)
        # if it's valid, it doesn't return anything
        self.assertIsNone(result)

        # bad uuid, it should trip
        random_uuid = str(uuid.uuid4())
        with self.assertRaises(ValidationError):
            validator(random_uuid)
