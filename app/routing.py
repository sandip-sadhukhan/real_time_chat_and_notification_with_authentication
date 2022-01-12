from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/user/notification/(?P<username>\w+)/$",
        consumers.UserNotificationConsumer.as_asgi(),
    ),
    path("ws/admin/notification/", consumers.AdminNotificationConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<username>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
