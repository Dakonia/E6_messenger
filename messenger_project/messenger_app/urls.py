from django.urls import path
from . import views

urlpatterns = [
    path('chats/<int:pk>/', views.chat_detail, name='chat_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('users/', views.user_list, name='user_list'),
    path('', views.index, name='index'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]

