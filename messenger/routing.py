from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('rooms/<int:room_id>/', consumers.MessengerConsumer),
]
