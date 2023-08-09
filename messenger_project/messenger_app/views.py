from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message, UserProfile, User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ChatForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def chat_list(request):
    chats = Chat.objects.all()
    return render(request, 'chat_list.html', {'chats': chats})

def chat_detail(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    messages = chat.message_set.all()
    participants = chat.participants.all()  # Получите список участников чата
    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages, 'participants': participants})


def user_profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'user_profile.html', {'user_profile': user_profile})

def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})


def index(request):
    if request.user.is_authenticated:  # Проверяем, авторизован ли пользователь
        chats = Chat.objects.all()
        chat_form = ChatForm()
        return render(request, 'index.html', {'chats': chats, 'chat_form': chat_form})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Перенаправляем авторизованного пользователя на index
        else:
            error_message = "Данного пользователя не существует. Пожалуйста, проверьте корректность введенных данных."
            return render(request, 'index.html', {'error_message': error_message})
    else:
        chat_form = ChatForm()
        return render(request, 'index.html', {'chat_form': chat_form})



def create_chat(request):
    if request.method == 'POST':
        chat_form = ChatForm(request.POST)
        if chat_form.is_valid():
            chat_form.save()
            return redirect('index')
    else:
        chat_form = ChatForm()

    return render(request, 'create_chat.html', {'chat_form': chat_form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Обрабатываем загруженные файлы
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                avatar=form.cleaned_data['avatar']
            )
            return redirect('index')  # Перенаправляем пользователя на главную страницу после успешной регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required  # Декоратор, требующий аутентификации пользователя
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})