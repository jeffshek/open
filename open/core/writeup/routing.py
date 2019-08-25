from django.conf.urls import url
from open.core.writeup import consumers

# can't actually test this yet without pytest

# these url patterns are prefixed with a /ws/ for load balancers to redirect traffic
websocket_urlpatterns = [
    url(
        r"^ws/async/writeup/text_generation/session/(?P<session_uuid>[^/]+)/$",
        consumers.AsyncWriteUpGPT2MediumConsumer,
    ),
    # this is a a quick test url when you need to restart the ml backend servers
    url(
        r"^ws/test/writeup/text_generation/session/(?P<session_uuid>[^/]+)/$",
        consumers.WriteUpGPT2MediumConsumerMock,
    ),
]
