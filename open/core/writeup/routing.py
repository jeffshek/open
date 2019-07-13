from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r"^ws/chat/(?P<room_name>[^/]+)/$", consumers.ChatConsumer),
    url(r"^wss/chat/(?P<room_name>[^/]+)/$", consumers.ChatConsumer),
]
