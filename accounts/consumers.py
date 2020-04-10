import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import JsonWebsocketConsumer
from .models import UserProfileInfo
from channels.consumer import AsyncConsumer
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async, async_to_sync


class UserConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add("users", self.channel_name))
        user = self.scope['user']
        if user.is_authenticated:
            sync_to_async(self.update_user_status(user, True))
            async_to_sync(self.send_status())

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard("users", self.channel_name))

        user = self.scope['user']
        if user.is_authenticated:
            sync_to_async(self.update_user_status(user, False))
            async_to_sync(self.send_status())

    def send_status(self):
        users = User.objects.all()
        html_users = render_to_string("accounts/includes/users.html", {'users': users})
        async_to_sync(self.send_json({
            "html_users": html_users,
        }))

    def update_user_status(self, user, status):
        return UserProfileInfo.objects.filter(user_id=user.pk).update(status=status)
