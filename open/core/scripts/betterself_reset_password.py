from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from open.users.models import User

"""
dpy runscript betterself_reset_password
"""


def run():
    user = User.objects.get(email="jeff@senrigan.io")
    url = reverse("rest_password_reset")

    client = APIClient()
    client.force_login(user)

    data = {"email": user.email}

    response = client.post(url, data=data)
