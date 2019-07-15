from django.conf.urls import url

from . import consumers

# this is prefixed with a /ws/ for load balancers to redirect traffic
websocket_urlpatterns = [
    url(r"^ws/chat/(?P<room_name>[^/]+)/$", consumers.ChatConsumer),
    url(
        r"^ws/writeup/session/(?P<session_uuid>[^/]+)/$",
        consumers.WriteUpSessionConsumer,
    ),
]
