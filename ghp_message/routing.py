from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import accounts.routing
import messenger.routing
from django.urls import path, re_path, include
from accounts.consumers import UserConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/accounts/", URLRouter(accounts.routing.websocket_urlpatterns)),
                path("ws/messenger/", URLRouter(messenger.routing.websocket_urlpatterns))
            ]
        )
    ),
})
