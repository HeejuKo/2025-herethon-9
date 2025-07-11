from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_list(request):
    user = request.user

    rooms = ChatRoom.objects.filter(Q(customer=user) | Q(expert=user)).prefetch_related('messages')

    room_data = []

    for room in rooms:
        last_msg = room.messages.last()
        unread_count = room.messages.filter(is_read=False).exclude(sender=user).count()
        last_activity = last_msg.created_at if last_msg else room.created_at

        room_data.append({
            'room': room,
            'last_msg': last_msg,
            'unread_count': unread_count,
            'last_activity': last_activity,
        })
        
    room_data.sort(key=lambda x: x['last_activity'], reverse=True)

    return render(request, 'chats/chat-list.html', {'room_data': room_data})

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
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
        return redirect('chats:chat_room', room_id=room.id)

    # 본인이 아닌 사람이 보낸 읽지 않은 메시지들을 읽음 처리
    room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    messages = room.messages.order_by('created_at')

    return render(request, 'chats/chat-room.html', {'room': room, 'messages': messages})