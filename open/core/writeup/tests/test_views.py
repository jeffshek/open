from open.core.writeup.constants import WriteUpResourceEndpoints
from open.utilities.testing_mixins import OpenDefaultTest


class WriteupViewTests(OpenDefaultTest):
    """
    dpy test core.writeup
    """

    VIEW_NAME = WriteUpResourceEndpoints.GENERATED_SENTENCE

    def test_this_point(self):
        pass
