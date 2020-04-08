from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Base(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChatRoom(Base):
    users = models.ManyToManyField(User, related_name="chatrooms")
    title = models.TextField(default="Room:")


class Message(Base):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-created_at').all()[:10]
