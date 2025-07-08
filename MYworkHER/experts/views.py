from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from matching.models import Matching
from accounts.models import User, UserType
from .models import Expert


@login_required
def expert_list(request):
    keyword = request.GET.get('keyword', '')
    experts = User.objects.filter(userType=UserType.EXPERT).select_related('expert_profile')

    if keyword:
        experts = experts.filter(
            Q(username__icontains=keyword) |
            Q(expert_profile__bio__icontains=keyword) |
            Q(expert_profile__description__icontains=keyword) |
            Q(expert_profile__category__icontains=keyword)
        )

    return render(request, 'experts/expert_list.html', {
        'experts' : experts,
        'keyword' : keyword,
    })

@login_required
def expert_detail(request, expert_id):
    expert = get_object_or_404(User, id=expert_id, userType=UserType.EXPERT)

    # 이번 달 예약 수 (현재 월 기준)
    from datetime import date
    today = date.today()
    monthly_reservation_count = Matching.objects.filter(
        expert=expert,
        date__year=today.year,
        date__month=today.month
    ).count()

    return render(request, 'experts/expert_detail.html', {
        'expert' : expert,
        'reservation_count' : monthly_reservation_count
    })