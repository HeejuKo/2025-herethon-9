from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_request(request, expert_id):
    expert = get_object_or_404(User, id=expert_id, userType='EXPERT')

    if request.user == expert: # 자신과의 채팅은 불가
        return redirect('matching:main')

    # 이미 존재하는 방이 있는지 확인
    room = ChatRoom.objects.filter(customer=request.user, expert=expert).first()
    if not room:
        room = ChatRoom.objects.create(customer=request.user, expert=expert)

    return redirect('chats:chat_room', room_id=room.id)

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    if request.user != room.customer and request.user != room.expert:
        return redirect('chats:chat_list')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ChatMessage.objects.create(room=room, sender=request.user, content=content)
            return redirect('chats:chat_room', room_id=room.id)

    messages = room.messages.order_by('created_at')

    return render(request, 'chats/chat-room.html', {'room': room, 'messages': messages})

@login_required
def chat_list(request):
    rooms = ChatRoom.objects.filter(customer=request.user) | ChatRoom.objects.filter(expert=request.user)
    rooms = rooms.order_by('-created_at')

    return render(request, 'chats/chat-list.html', {'rooms': rooms})