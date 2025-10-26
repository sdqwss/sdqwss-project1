from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('room/<int:room_id>/', views.room_view, name='room'),
    path('user/<str:username>/', views.private_chat, name='private_chat'),
    path('create/group/', views.create_group_room, name='create_group_room'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.user_list, name='user_list'),
]
