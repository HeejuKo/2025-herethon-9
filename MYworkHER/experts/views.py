from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from matching.models import Matching
from accounts.models import RegionChoices, User, UserType
from .models import CategoryChoices, Expert

# 키워드 검색 시 한글 - 영문 매핑
def get_category_value_by_label(keyword):
    for value, label in CategoryChoices.choices:
        if keyword in label:
            return value
    return None

# 지역구 필터링 영문 매핑
def get_region_value_by_label(label):
    for value, display in RegionChoices.choices:
        if label == display:  # 예: '마포구' == '마포구'
            return value       # 반환: 'MAPO'
    return None

@login_required
def expert_list(request):
    keyword = request.GET.get('keyword', '')
    region_filters = request.GET.getlist('region')
    experience_filters = request.GET.getlist('experience')
    badge_filter = request.GET.get('badge')
    experts = User.objects.filter(userType=UserType.EXPERT).select_related('expert_profile')

    # 키워드 검색
    if keyword:
        category_val = get_category_value_by_label(keyword)
        category_q = Q()
        if category_val:
            category_q = Q(expert_profile__category=category_val)

        experts = experts.filter(
            Q(username__icontains=keyword) |
            Q(expert_profile__bio__icontains=keyword) |
            Q(expert_profile__description__icontains=keyword) |
            category_q
        )
    
    # 지역 필터링
    if region_filters:
        # 한글 지역명(라벨) → 영문 코드(value)로 변환
        region_values = [get_region_value_by_label(label) for label in region_filters]
        region_values = [r for r in region_values if r]
        experts = experts.filter(region__in=region_values)

    # 경력 필터링
    if experience_filters:
        queries = Q()
        for e in experience_filters:
            if e == '0':        # 1년 미만
                queries |= Q(expert_profile__experience__lt=1)
            elif e == '1':      # 1년 이상 ~ 3년 미만
                queries |= Q(expert_profile__experience__gte=1, expert_profile__experience__lt=3)
            elif e == '3':      # 3년 이상 ~ 5년 미만
                queries |= Q(expert_profile__experience__gte=3, expert_profile__experience__lt=5)
            elif e == '5':      # 5년 이상
                queries |= Q(expert_profile__experience__gte=5)
        experts = experts.filter(queries)
    
    # 인증배지 필터링
    if badge_filter == 'true':
        experts = experts.filter(expert_profile__badge='VERIFIED')

    return render(request, 'experts/expert_list.html', {
        'experts' : experts,
        'keyword' : keyword,
        'selected_region' : region_filters,
        'selected_experience': experience_filters,
        'badge': badge_filter == 'true',
        'region_list' : [r[1] for r in RegionChoices.choices]  # 지역 필터를 한글 기준으로 전달
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

    # 카테고리를 한글로 출력
    category_display = expert.expert_profile.get_category_display() if expert.expert_profile.category else "미등록"

    # 지역구를 한글로 출력
    region_display = expert.get_region_display() if expert.region else "미등록" 

    return render(request, 'experts/expert_detail.html', {
        'expert' : expert,
        'category_display' : category_display,
        'region_display' : region_display,
        'reservation_count' : monthly_reservation_count
    })