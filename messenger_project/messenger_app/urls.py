from django.urls import path
from . import views

urlpatterns = [
    # URL-маршрут для списка чатов
    # path('', views.chat_list, name='chat_list'),

    # URL-маршрут для просмотра и управления отдельным чатом
    path('chats/<int:pk>/', views.chat_detail, name='chat_detail'),

    # URL-маршрут для просмотра профиля пользователя
    path('profile/', views.user_profile, name='user_profile'),

    # URL-маршрут для списка других пользователей
    path('users/', views.user_list, name='user_list'),
    path('', views.index, name='index'),
]
