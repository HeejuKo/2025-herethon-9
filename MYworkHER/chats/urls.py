from django.urls import path
from .views import *

app_name = 'chats'

urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('request/<int:expert_id>/', chat_request, name='chat_request'),
    path('<int:room_id>/', chat_room, name='chat_room'),
]
