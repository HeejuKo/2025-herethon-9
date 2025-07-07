from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Matching
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

def main(request):
    return render(request, 'matching/main.html')

@csrf_exempt
# @login_required
def create_matching(request):
    if request.method == 'POST':
        expert_id = request.POST.get('expert_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes', '')

        # 중복 예약 확인
        if Matching.objects.filter(expert_id=expert_id, date=date, time=time).exists():
            return render(request, 'matching/matching.html', {
                'error': '해당 시간에 이미 예약이 존재합니다.'
            })

        try:
            customer = User.objects.get(pk=10)  # 테스트용 customer 지정
            # customer = request.user
            expert = User.objects.get(pk=expert_id)
        except User.DoesNotExist:
            return render(request, 'matching/matching.html', {
                'error': '존재하지 않는 사용자입니다.'
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
    
    return render(request, 'matching/matching.html')


def matching_success(request):
    return render(request, 'matching/success.html')