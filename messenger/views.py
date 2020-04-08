import json
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'message/index.html')


@login_required
def room(request, room_name):
    return render(request, 'message/messenger.html', {
        'room_name': room_name,
        'username': request.user.username,
    })
