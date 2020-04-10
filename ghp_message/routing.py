from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import messenger.routing
from django.urls import path
from accounts.consumers import UserConsumer
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path("", UserConsumer),
            ]
        )
    ),
})
# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             messenger.routing.websocket_urlpatterns
#         )
#     ),
# })
