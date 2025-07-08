from django.shortcuts import render
from django.contrib.auth import get_user_model

from accounts.models import UserType
from .models import Matching
from django.contrib.auth.decorators import login_required

User = get_user_model()

def main(request):
    expert = User.objects.get(id=3)
    return render(request, 'matching/main.html', {'expert': expert})

@login_required
def create_matching(request):
    experts = User.objects.filter(userType=UserType.EXPERT)

    if request.method == 'POST':
        expert_id = request.POST.get('expert_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes', '')

        # 중복 예약 확인
        if Matching.objects.filter(expert_id=expert_id, date=date, time=time).exists():
            return render(request, 'matching/matching.html', {
                'error': '해당 시간에 이미 예약이 존재합니다.',
                'expert' : expert
            })

        try:
            customer = User.objects.get(pk=10)  # 테스트용 customer 지정
            # customer = request.user
            expert = User.objects.get(pk=expert_id)
        except User.DoesNotExist:
            return render(request, 'matching/matching.html', {
                'error': '존재하지 않는 사용자입니다.',
                'experts': experts
            })

        reservation = Matching.objects.create(
            customer=customer,
            expert=expert,
            date=date,
            time=time,
            notes=notes
        )

        return render(request, 'matching/success.html', {
            'reservation': reservation
        })
    
    return render(request, 'matching/matching.html', {'experts': experts})


def matching_success(request):
    return render(request, 'matching/success.html')