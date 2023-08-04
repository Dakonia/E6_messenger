from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message, UserProfile, User
from .forms import ChatForm
from django.contrib.auth.forms import UserCreationForm


def chat_list(request):
    chats = Chat.objects.all()
    return render(request, 'chat_list.html', {'chats': chats})

def chat_detail(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    messages = Message.objects.filter(chat=chat)
    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages})

def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user_profile.html', {'user_profile': user_profile})

def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})

def index(request):
    # Обработка регистрации пользователя
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    # Получение списка чатов
    chats = Chat.objects.all()

    # Обработка создания нового чата
    if request.method == 'POST':
        chat_form = ChatForm(request.POST)
        if chat_form.is_valid():
            chat_form.save()
            return redirect('index')
    else:
        chat_form = ChatForm()

    return render(request, 'index.html', {'chats': chats, 'chat_form': chat_form})