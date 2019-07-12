from rest_framework.reverse import reverse
from test_plus import APITestCase

from open.core.writeup.constants import WriteUpResourceEndpoints
from open.users.factories import UserFactory
from open.users.models import User


class OpenDefaultTest(APITestCase):
    """
    Note: This will also run itself once too ...
    This is a bit of an antipattern, I should separate as a mixin better
    But it makes harder to read
    """

    # just use a random view
    VIEW_NAME = WriteUpResourceEndpoints.GENERATED_SENTENCE

    def setUp(self):
        self.registered_user = User.objects.get(id=self.registered_user_id)
        self.staff_user = UserFactory(is_staff=True)

    @classmethod
    def set_reversed_url(cls):
        # make this a method so that it can be overriden
        # for any specific urls
        cls.url = reverse(cls.VIEW_NAME)

    @classmethod
    def setUpTestData(cls):
        registered_user = UserFactory(is_staff=False)
        cls.registered_user_id = registered_user.id

        staff_user = UserFactory(is_staff=True)
        cls.staff_user_id = staff_user.id

        cls.set_reversed_url()

    def test_get_primary_view(self):
        self.get(self.url)
        self.response_200()
