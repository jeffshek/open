from open.users.factories import UserFactory
from open.users.models import User


class TestCaseMixins:
    def setUp(self):
        self.registered_user = User.objects.get(id=self.registered_user_id)
        self.staff_user = UserFactory(is_staff=True)

    @classmethod
    def setupTestData(cls):
        registered_user = UserFactory(is_staff=False)
        cls.registered_user_id = registered_user.id

        staff_user = UserFactory(is_staff=True)
        cls.staff_user_id = staff_user.id

    def setUpDefault(self):
        self.registered_user = UserFactory(is_staff=False)
        self.staff_user = UserFactory(is_staff=True)
