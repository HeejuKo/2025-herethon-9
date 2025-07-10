from django.db.models import Count, Q
from datetime import datetime, timedelta
from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from accounts.models import UserType
from .models import Matching
from chats.models import ChatRoom
from django.contrib.auth.decorators import login_required

User = get_user_model()

def main(request):

    current_month = datetime.now().month
    top_experts = (
        User.objects.filter(userType=UserType.EXPERT)
        .annotate(
            monthly_count = Count(
                'expert_matching',
                filter=Q(expert_matching__date__month=current_month)
            )
        )
        .order_by('-monthly_count')[:3]
    )

    return render(request, 'matching/main.html', {
        'top_experts': top_experts,
    })

# 전문가 id를 받아와 예약 진행
def get_selected_expert(expert_id):
    try:
        return User.objects.get(id=expert_id, userType=UserType.EXPERT)
    except User.DoesNotExist:
        return None
    
def get_available_dates():
    today = datetime.today()
    return [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

def get_available_times():
    return [f"{hour:02d}:00" for hour in range(9, 21)]  # 09:00 ~ 20:00

# 예약 생성
@login_required
def create_matching(request):
    experts = User.objects.filter(userType=UserType.EXPERT)
    selected_expert = None

    if request.method == 'POST':
        expert_id = request.POST.get('expert_id')
        date_list = request.POST.get('dates', '').split(',')
        time_list = request.POST.get('times', '').split(',')
        notes = request.POST.get('notes', '')

        selected_expert = get_selected_expert(expert_id)

        if selected_expert:
            request.session['temp_matching'] = {
                'expert_id' : expert_id,
                'dates' : date_list,
                'times' : time_list,
                'notes' : notes
            }

            print("🔒 세션 저장 완료:", request.session['temp_matching'])

            return redirect('matching:reserve-confirm', matching_id=0)
    
    else:
        expert_id = request.GET.get('expert_id')
        if expert_id:
            selected_expert = get_selected_expert(expert_id)

    return render(request, 'matching/reserve.html', {
        'experts': experts,
        'selected_expert': selected_expert,
        'available_dates': get_available_dates(),
        'available_times': get_available_times(),
    })

# 예약 정보 조회
@login_required
def matching_detail(request, matching_id):
    temp = request.session.get('temp_matching')
    if not temp:
        messages.error(request, "예약 정보가 없습니다.")
        return redirect('matching:create-matching')

    expert = get_selected_expert(temp['expert_id'])

    return render(request, 'matching/reserve_confirm.html', {
        'expert': expert,
        'date_matchings': temp['dates'],
        'time_matchings': temp['times'],
        'notes': temp['notes'],
    })

# 예약 수정
@login_required
def edit_matching(request, matching_id):
    experts = User.objects.filter(userType=UserType.EXPERT)

    if request.method == 'POST':
        # 수정된 값들을 받아 다시 저장
        expert_id = request.POST.get('expert_id')
        date_list = request.POST.getlist('dates[]')
        time_list = request.POST.getlist('times[]')
        notes = request.POST.get('notes', '')

        selected_expert = get_selected_expert(expert_id)

        if selected_expert:
            request.session['temp_matching'] = {
                'expert_id': expert_id,
                'dates': date_list,
                'times': time_list,
                'notes': notes
            }
            return redirect('matching:reserve_confirm', matching_id=0)
        else:
            return render(request, 'matching/reserve.html', {
                'experts': experts,
                'selected_expert': None,
                'available_dates': get_available_dates(),
                'available_times': get_available_times(),
                'selected_dates': date_list,
                'selected_times': time_list,
                'notes': notes,
                'error': '선택한 전문가가 존재하지 않습니다.'
            })


    temp = request.session.get('temp_matching')
    if not temp:
        return redirect('matching:create-matching')

    selected_expert = get_selected_expert(temp['expert_id'])

    return render(request, 'matching/reserve.html', {
        'experts': experts,
        'selected_expert': selected_expert,
        'available_dates': get_available_dates(),
        'available_times': get_available_times(),
        'selected_dates': temp['dates'],
        'selected_times': temp['times'],
        'notes': temp['notes'],
    })

# 예약 확정 및 저장
@login_required
def matching_success(request, matching_id):
    temp = request.session.pop('temp_matching', None)

    if not temp:
        return redirect('matching:create-matching')
    
    customer = request.user
    expert = get_selected_expert(temp['expert_id'])
    date_list = temp.get('dates')
    time_list = temp['times']
    notes = temp['notes']

    new_matchings = []
    try:
        for date_str, time_str in product(date_list, time_list):
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()
            new_matchings.append(Matching(customer=customer, expert=expert, date=date, time=time, notes=notes))
    except ValueError:
        pass

    Matching.objects.bulk_create(new_matchings)
    chat_room, _ = ChatRoom.objects.get_or_create(customer=customer, expert=expert)

    return render(request, 'matching/success.html', {
        'expert': expert,
        'chatroom_id': chat_room.id if chat_room else None,
        'matchings': new_matchings[0]
    })