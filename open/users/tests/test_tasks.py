from celery.result import EagerResult
from django.test import TestCase

from open.users.factories import UserFactory
from open.users.models import User

from open.users.tasks import get_users_count


class TestUserCeleryTasks(TestCase):
    def test_user_count(self):
        User.objects.all().delete()
        """A basic test to execute the get_users_count Celery task."""
        UserFactory.create_batch(3)

        task_result = get_users_count.delay()

        self.assertIsInstance(task_result, EagerResult)
        self.assertEqual(task_result.result, 3)
