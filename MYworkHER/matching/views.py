from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from accounts.models import UserType
from .models import Matching
from chats.models import ChatRoom
from django.contrib.auth.decorators import login_required

User = get_user_model()

# 전문가 id를 받아와 예약 진행
def get_selected_expert(expert_id):
    try:
        return User.objects.get(id=expert_id, userType=UserType.EXPERT)
    except User.DoesNotExist:
        return None
    
def main(request):
    return render(request, 'matching/main.html')

@login_required
def create_matching(request):
    experts = User.objects.filter(userType=UserType.EXPERT)
    selected_expert = None
    error_message = None

    if request.method == 'POST':
        expert_id = request.POST.get('expert_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes', '')

        selected_expert = get_selected_expert(expert_id)

        if selected_expert:
            try:
                customer = request.user
                expert = selected_expert

                matching = Matching.objects.create(
                    customer=customer,
                    expert=expert,
                    date=date,
                    time=time,
                    notes=notes
                )

                chat_room, _ = ChatRoom.objects.get_or_create(
                    customer=customer,
                    expert=expert
                )

                return redirect('matching:matching-detail', matching_id=matching.id)

            except Exception as e:
                error_message = '예약 중 오류가 발생했습니다.'

    else:
        # 전문가 상세 페이지에서 전문가 id를 받아와 예약 진행
        expert_id = request.GET.get('expert_id')
        if expert_id:
            selected_expert = get_selected_expert(expert_id)

    return render(request, 'matching/matching.html', {
        'experts': experts,
        'selected_expert': selected_expert,
    })

# 예약 확인
@login_required
def matching_detail(request, matching_id):
    matching = get_object_or_404(Matching, id=matching_id)
    expert = matching.expert

    context = {
        'matching' : matching,
        'expert' : expert,
    }

    return render(request, 'matching/matching-detail.html', context)

# 예약 수정
@login_required
def edit_matching(request, matching_id):
    matching = get_object_or_404(Matching, id=matching_id)
    experts = User.objects.filter(userType=UserType.EXPERT)

    selected_expert = matching.expert

    if request.method=='POST':
        expert_id = request.POST.get('expert_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes', '')

        updated_expert = get_selected_expert(expert_id)

        if updated_expert:
            matching.expert = updated_expert
            matching.date = date
            matching.time = time
            matching.notes = notes
            matching.save()
            return redirect('matching:matching-detail', matching_id=matching.id)
        else:
            selected_expert = None  # 선택 오류시 초기화

    return render(request, 'matching/matching.html', {
        'experts': experts,
        'selected_expert': selected_expert,
        'matching': matching,
    })

@login_required
def matching_success(request, matching_id):
    matching = get_object_or_404(Matching, id=matching_id)
    expert = matching.expert

    # 예약된 사용자와 전문가 채팅방 가져오기
    chat_room = ChatRoom.objects.filter(
        customer=matching.customer,
        expert=expert
    ).first()

    return render(request, 'matching/success.html', {
        'matching': matching,
        'expert' : expert,
        'chatroom_id': chat_room.id if chat_room else None
    })