import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import UserProfileInfo
from .models import ChatRoom, Message


class MessengerConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        try:
            messages = Message.objects.select_related('author').filter(chatroom_id=self.room_id).order_by('-created_at')[:20:-1]
            content = {
                'command': 'messages',
                'messages': self.messages_to_json(messages),
                'room_id': self.room_id
            }
            self.send_message(content)
        except:
            self.disconnect(close_code=500)

    def new_message(self, data):
        try:
            author_user = self.current_user
            room = ChatRoom.objects.get(id=int(self.room_id))
            content = data['message']
            message = Message.objects.create(author=author_user, content=content, chatroom=room)
            room.updated_at = timezone.now
            room.save()
            content = {
                'command': 'new_message',
                'message': self.message_to_json(message),
                'room_id': self.room_id
            }
            return self.send_messenger_message(content)
        except:
            self.disconnect(close_code=500)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.author.username,
            'content': message.content,
            'created_at': str(message.created_at),
            'room_id': str(message.chatroom_id)
        }

    def check_connect(self, data):
        content = {
            'command': 'check_connect'
        }
        self.send_message(content)


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'check_connect': check_connect
    }

    def connect(self):
        self.current_user = self.scope["user"]
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        try:
            room = ChatRoom.objects.prefetch_related("users").get(id=int(self.room_id))
            self.room = room
            if not room.users.filter(id=self.current_user.id).exists():
                self.close()
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        except:
            self.close()



    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_messenger_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))


class UserOnlineConsumer(WebsocketConsumer):
    def fetch_users(self, data):
        users = User.objects.select_related("profile").all()
        content = {
            'command': 'fetch_users',
            'users': self.users_to_json(users)
        }
        async_to_sync(self.send_message(content))
        pass

    def users_to_json(self, users):
        result = []
        for user in users:
            result.append(self.user_to_json(user))
        return result
        pass

    def user_to_json(self, user):
        try:
            return {
                'id': user.id,
                'username': user.username,
                'online': str(user.profile.status)
            }
        except:
            return {
                'id': user.id,
                'username': user.username,
                'online': 'unknown'
            }
        pass

    def new_user_online(self, data):
        try:
            UserProfileInfo.objects.filter(user_id=self.current_user.id).update(status=True)
            content = {
                'command': 'new_user_online',
                'user': self.user_to_json(self.current_user)
            }
            return self.send_messenger_message(content)
        except:
            content = {
                'command': 'new_user_online',
                'user': self.user_to_json(self.current_user)
            }
            return self.send_messenger_message(content)



    commands = {
        "fetch_users": fetch_users,
        "new_user_online": new_user_online,
    }

    def connect(self):
        self.current_user = self.scope["user"]
        self.room_group_name = "users_chanel"
        if self.current_user.is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
            self.new_user_online({})
        else:
            self.close()

    def disconnect(self, close_code):
        try:
            current_user = self.scope['user']
            self.update_user_status(current_user, False)
            content = {
                'command': 'new_user_offline',
                'user': self.user_to_json(current_user)
            }
            return sync_to_async(self.send_messenger_message(content))
        except:
            pass
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_messenger_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    def update_user_status(self, user, status):
        return UserProfileInfo.objects.filter(user_id=user.id).update(status=status)
