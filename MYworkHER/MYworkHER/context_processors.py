# from chats.models import ChatMessage

# def unread_chat_count(request):
#     if request.user.is_authenticated:
#         count = ChatMessage.objects.filter(
#             is_read=False
#         ).exclude(sender=request.user).count()
#         return {'unread_chat_total': count}
#     return {}

from chats.models import ChatRoom, ChatMessage

def unread_chat_count(request):
    if request.user.is_authenticated:
        # 1. 내가 참여 중인 채팅방 찾기
        my_rooms = ChatRoom.objects.filter(
            customer=request.user
        ) | ChatRoom.objects.filter(
            expert=request.user
        )

        # 2. 내 채팅방에서, 내가 보낸 게 아니고 안 읽은 메시지 찾기
        count = ChatMessage.objects.filter(
            room__in=my_rooms,
            is_read=False
        ).exclude(sender=request.user).count()

        return {'unread_chat_total': count}
    return {}