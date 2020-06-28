from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import URLPattern, URLResolver

User = get_user_model()

"""
python manage.py test --pattern="*test_urls_configured.py"
"""

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])


def list_urls(lis, acc=None):
    # ripped from stackoverflow
    if acc is None:
        acc = []
    if not lis:
        return
    data = lis[0]
    if isinstance(data, URLPattern):
        yield acc + [str(data.pattern)]
    elif isinstance(data, URLResolver):
        yield from list_urls(data.url_patterns, acc + [str(data.pattern)])
    yield from list_urls(lis[1:], acc)


class TestAPIPostfixSlash(TestCase):
    """
    django will automatically postfix requests with a trailing slash from API requests
    ie. if someone makes a request on api/resource, django will search the urls for api/resource/

    to support this, always add a trailing slash at urls

    otherwise, you can have some weird browser issues with safari refusing to make requests
    """

    def test_api_urls_ends_with_slash(self):

        for url_pattern in list_urls(urlconf.urlpatterns):
            """
            returns similar to below

            ['admin/', 'core/writeupflaggedprompt/', '<path:object_id>/']
            ['api/writeup/v1/', 'generated_sentence/']
            """
            url_pattern_serialized = "".join(url_pattern)

            if not url_pattern_serialized:
                continue

            is_api_endpoint = url_pattern_serialized[:3] == "api"
            ends_with_forward_slash = url_pattern_serialized[-1] == "/"

            if is_api_endpoint:
                if not ends_with_forward_slash:
                    raise ValueError(f"{url_pattern_serialized} does not end with a /!")
