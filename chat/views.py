from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Message, ChatRoom


def home(request):
    messages = Message.objects.all().order_by('timestamp')
    return render(request, 'chat/chat.html', {
        'messages': messages
    })


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            return render(request, 'chat/chat.html')

        return render(request, 'chat/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'chat/login.html')

def rooms(request):
    chat_rooms = ChatRoom.objects.all().order_by('name')
    return render(request, 'chat/rooms.html', {
        'rooms': chat_rooms
    })

def room_chat(request, room_name):
    room = ChatRoom.objects.get(name=room_name)
    messages = Message.objects.filter(room=room).order_by('timestamp')

    return render(request, 'chat/chat.html', {
        'room': room,
        'messages': messages
    })