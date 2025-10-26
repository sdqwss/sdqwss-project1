from django.contrib.auth.models import User
from .forms import GroupRoomForm
from django import forms
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Message


def home(request):
    if request.user.is_authenticated:
        return redirect('room_list')
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            general_room, created = Room.objects.get_or_create(name='Общий')
            general_room.members.add(user)
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('room_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def room_list(request):
    rooms = request.user.chat_rooms.all()
    return render(request, 'chat/room_list.html', {'rooms': rooms})


@login_required
def room_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user not in room.members.all():
        messages.error(request, "Вы не состоите в этом чате.")
        return redirect('room_list')

    if request.method == "POST":
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(room=room, user=request.user, content=content)
            return redirect('room', room_id=room_id)

    messages_qs = room.messages.select_related('user').all()
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages_qs
    })


@login_required
def profile(request):
    return render(request, 'profile.html')

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название чата', 'autofocus': True})
        }

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            room.members.add(request.user)
            messages.success(request, f'Чат "{room.name}" создан!')
            return redirect('room', room_name=room.name)
    else:
        form = RoomForm()
    return render(request, 'chat/create_room.html', {'form': form})

@login_required
def create_group_room(request):
    if request.method == 'POST':
        form = GroupRoomForm(request.POST, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Групповой чат создан!')
            return redirect('room_list')
    else:
        form = GroupRoomForm(current_user=request.user)
    return render(request, 'chat/create_group_room.html', {'form': form})

@login_required
def private_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        messages.error(request, "Нельзя создать чат с самим собой.")
        return redirect('room_list')

    room = Room.get_private_room(request.user, other_user)
    return redirect('room',room.id)

@login_required
def user_list(request):
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'chat/user_list.html', {'users': users})

