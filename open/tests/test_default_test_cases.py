from open.core.writeup.constants import WriteUpResourceEndpoints
from open.utilities.testing_mixins import OpenDefaultTest


class TestDefaultOpenTestCase(OpenDefaultTest):
    # just use a random view
    VIEW_NAME = WriteUpResourceEndpoints.GENERATED_SENTENCE

    def test_registered_user_exists(self):
        self.assertIsNotNone(self.registered_user)

    def test_staff_user_exists(self):
        self.assertIsNotNone(self.staff_user)
