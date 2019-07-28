from django.conf.urls import url
from open.core.writeup import consumers

# these url patterns are prefixed with a /ws/ for load balancers to redirect traffic
websocket_urlpatterns = [
    url(
        r"^ws/writeup/gpt2_medium/session/(?P<session_uuid>[^/]+)/$",
        consumers.WriteUpGPT2MediumConsumer,
    ),
    url(
        r"^ws/test/writeup/gpt2_medium/session/(?P<session_uuid>[^/]+)/$",
        consumers.WriteUpGPT2MediumConsumerMock,
    ),
]
