import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction, DatabaseError
from django.db.models import Q


from .models import Message, ChatRoom

User = get_user_model()


def index(request):
    return render(request, 'message/index.html')


@login_required
def room(request):
    current_user = request.user
    chatrooms = current_user.chatrooms.order_by('-updated_at').all()
    return render(request, 'message/messenger.html', {
        'current_user': current_user,
        'chatrooms': chatrooms
    })


@transaction.atomic
def create_room(request, user_id):
    user = get_object_or_404(User, id=user_id)
    own_user = request.user
    chat_room = ChatRoom.objects.create(title=f'{user.username}, {own_user.username}')
    try:
        with transaction.atomic():
            chat_room.save()
            chat_room.users.add(own_user, user)
    except IntegrityError:
        return redirect("messenger:index")

    return redirect("/")


def room_add_user(request, room_id, user_id):
    try:
        chatroom = ChatRoom.objects.prefetch_related("users").get(id=room_id)
    except:
        return redirect("/")
    user = get_object_or_404(User, id=user_id)
    own_user = request.user
    if chatroom.users.filter(Q(id=own_user.id)).exists() and not chatroom.users.filter(Q(id=user_id)).exists():
        chatroom.title+=f', {user.username}'
        chatroom.users.add(user)
        return redirect("messenger:index")

    return redirect("/")

