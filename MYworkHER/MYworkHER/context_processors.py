from chats.models import ChatMessage

def unread_chat_count(request):
    if request.user.is_authenticated:
        count = ChatMessage.objects.filter(
            is_read=False
        ).exclude(sender=request.user).count()
        return {'unread_chat_total': count}
    return {}