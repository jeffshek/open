from open.core.writeup.constants import WriteUpResourceEndpoints
from open.utilities.testing_mixins import OpenDefaultTest


class WriteupViewTests(OpenDefaultTest):
    """
    dpy test core.writeup
    """

    VIEW_NAME = WriteUpResourceEndpoints.GENERATED_SENTENCE
    VIEW_NEEDS_LOGIN = False

    def test_get_view(self):
        response = self._get_response_data()
        self.assertTrue("prompt" in response)
