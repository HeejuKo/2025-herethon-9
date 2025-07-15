import random
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from chats.models import ChatRoom
from matching.models import Matching
from accounts.models import *
from .models import *
from category.constants import *

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
def expert_main(request):
    # 추천 전문가: 인증 배지를 가진 사람 중 최대 3명 랜덤
    verified_experts = Expert.objects.filter(badge=BadgeChoices.VERIFIED.value)
    if verified_experts.exists():
        recommended_experts = random.sample(list(verified_experts), min(3, verified_experts.count()))
    else:
        recommended_experts = []

    return render(request, 'experts/expert.html', {
        'recommended_experts': recommended_experts
    })

def apply_region_filter(queryset, region_filters, seoul_all):
    if region_filters and not seoul_all:
        region_values = list(filter(None, (get_region_value_by_label(label) for label in region_filters)))
        return queryset.filter(user__region__in=region_values)
    return queryset

def apply_experience_filter(queryset, experience_filters):
    if experience_filters:
        queries = Q()
        for e in experience_filters:
            if e == '0':
                queries |= Q(experience__lt=1)
            elif e == '1':
                queries |= Q(experience__gte=1, experience__lt=3)
            elif e == '3':
                queries |= Q(experience__gte=3, experience__lt=5)
            elif e == '5':
                queries |= Q(experience__gte=5)
        return queryset.filter(queries)
    return queryset

def apply_badge_filter(queryset, badge_filter):
    if badge_filter == 'true':
        return queryset.filter(badge=BadgeChoices.VERIFIED)
    return queryset

@login_required
def expert_search(request):
    keyword = request.GET.get('keyword', '')
    region_filters = request.GET.getlist('region')
    experience_filters = request.GET.getlist('experience')
    badge_filter = request.GET.get('badge')
    seoul_all = request.GET.get('seoul_all') == 'true'
    show_all = request.GET.get('show_all') == 'true'

    experts_qs = Expert.objects.select_related('user').all()

    # 🔍 키워드 검색
    if keyword:
        category_val = get_category_value_by_label(keyword)
        category_q = Q(category=category_val) if category_val else Q()
        experts_qs = experts_qs.filter(
            Q(user__nickname__icontains=keyword) |
            Q(bio__icontains=keyword) |
            Q(description__icontains=keyword) |
            category_q
        )

    # 🔎 필터 적용
    experts_qs = apply_region_filter(experts_qs, region_filters, seoul_all)
    experts_qs = apply_experience_filter(experts_qs, experience_filters)
    experts_qs = apply_badge_filter(experts_qs, badge_filter)

    total_count = experts_qs.count()
    experts = list(experts_qs[:10]) if not show_all else list(experts_qs)

    return render(request, 'experts/expert_search.html', {
        'experts': experts,
        'total_count': total_count,
        'keyword': keyword,
        'selected_region': region_filters,
        'selected_experience': experience_filters,
        'badge': badge_filter == 'true',
        'show_all': show_all,
        'seoul_all': seoul_all,
        'region_list': [r[1] for r in RegionChoices.choices],
        'experience_options': [
            ('0', '1년 미만'),
            ('1', '1년~3년'),
            ('3', '3년~5년'),
            ('5', '5년 이상'),
        ],
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

    chatroom = ChatRoom.objects.filter(
        Q(customer=request.user, expert=expert) |
        Q(customer=expert, expert=request.user)
    ).first()

    return render(request, 'experts/expert_detail.html', {
        'expert' : expert,
        'category_display' : category_display,
        'region_display' : region_display,
        'reservation_count' : monthly_reservation_count,
        'chatroom_id': chatroom.id if chatroom else None,
    })