import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from matching.models import Matching
from accounts.models import RegionChoices, User, UserType
from .models import BadgeChoices, CategoryChoices, Expert

def category_list(request):
    return render(request, 'experts/category.html')  # 상위 카테고리 클릭 페이지

@login_required
def subcategory_list(request, category):
    # 예: 'appliance'를 전달받았을 때 하위 카테고리 및 전문가 수 조회
    category_map = {
        'appliance': '가전/수리',
        'health': '헬스/스포츠',
        'business': '컨설팅/비즈니스',
        'lifestyle': '생활/라이프',
    }

    label = category_map.get(category)

    # 하위 카테고리 임시
    subcategories = [
        {'name': '하위 카테고리1', 'count': 122},
        {'name': '하위 카테고리2', 'count': 122},
    ]

    return render(request, 'experts/subcategory.html', {
        'category': category,
        'label': label,
        'subcategories': subcategories
    })

def category_list(request):
    category_enum_map = {
        'appliance': ('가전/수리', CategoryChoices.APPLIANCE, ['세탁기', '에어컨']),
        'health': ('헬스/스포츠', CategoryChoices.HEALTH, ['헬스트레이너', '요가']),
        'business': ('컨설팅/비즈니스', CategoryChoices.BUSINESS, ['경영', '세무']),
        'lifestyle': ('생활/라이프', CategoryChoices.LIFESTYLE, ['청소', '인테리어']),
    }

    categories = {}

    for key, (label, enum_value, sub_list) in category_enum_map.items():
        subcategories = []
        for sub in sub_list:
            count = Expert.objects.filter(category=enum_value).count()  # 하위 필터 없다면 상위 기준으로
            subcategories.append({'name': sub, 'count': count})
        categories[key] = {
            'label': label,
            'subcategories': subcategories
        }

    return render(request, 'experts/category.html', {'categories': categories})

@login_required
def expert_category(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')

    region_filters = request.GET.getlist('region')
    experience_filters = request.GET.getlist('experience')
    badge_filter = request.GET.get('badge')
    show_all = request.GET.get('show_all') == 'true'

    category_enum_map = {
        'appliance': (CategoryChoices.APPLIANCE, '가전/수리'),
        'health': (CategoryChoices.HEALTH, '헬스/스포츠'),
        'business': (CategoryChoices.BUSINESS, '컨설팅/비즈니스'),
        'lifestyle': (CategoryChoices.LIFESTYLE, '생활/라이프'),
    }

    category_value = None
    category_label = None
    experts_qs = Expert.objects.select_related('user').all()

    if category in category_enum_map:
        category_value, category_label = category_enum_map[category]
        experts_qs = experts_qs.filter(category=category_value)

    # 하위 카테고리는 적용 X
    # if subcategory:
        # experts_qs = experts_qs.filter(description__icontains=subcategory)

    # 지역 필터링
    if region_filters:
        region_values = [get_region_value_by_label(label) for label in region_filters]
        region_values = [r for r in region_values if r]
        experts_qs = experts_qs.filter(user__region__in=region_values)

    # 경력 필터링
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
        experts_qs = experts_qs.filter(queries)

    # 인증 배지 필터링
    if badge_filter == 'true':
        experts_qs = experts_qs.filter(badge=BadgeChoices.VERIFIED)

    total_count = experts_qs.count()
    experts = list(experts_qs[:10]) if not show_all else list(experts_qs)

    return render(request, 'experts/category_expert.html', {
        'experts': experts,
        'total_count': total_count,
        'category_label': category_label,
        'subcategory_label': subcategory,
        'selected_region': region_filters,
        'selected_experience': experience_filters,
        'badge': badge_filter == 'true',
        'show_all': show_all,
        'region_list': [r[1] for r in RegionChoices.choices],
    })


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

# 전문가 찾기 - 검색, 필터링
@login_required
def expert_list(request):
    keyword = request.GET.get('keyword', '')
    region_filters = request.GET.getlist('region')
    experience_filters = request.GET.getlist('experience')
    badge_filter = request.GET.get('badge')
    show_all = request.GET.get('show_all') == 'true'

    no_filter_applied = not keyword and not region_filters and not experience_filters and not badge_filter

    experts = []
    total_count = 0

    if not no_filter_applied:
        experts_qs = Expert.objects.select_related('user').all()

        # 키워드 검색
        if keyword:
            category_val = get_category_value_by_label(keyword)
            category_q = Q()
            if category_val:
                category_q = Q(category=category_val)

            experts_qs = experts_qs.filter(
                Q(user__username__icontains=keyword) |
                Q(bio__icontains=keyword) |
                Q(description__icontains=keyword) |
                category_q
            )

        # 지역 필터링
        if region_filters:
            # 한글 지역명(라벨) → 영문 코드(value)로 변환
            region_values = [get_region_value_by_label(label) for label in region_filters]
            region_values = [r for r in region_values if r]
            experts_qs = experts_qs.filter(user__region__in=region_values)

        # 경력 필터링
        if experience_filters:
            queries = Q()
            for e in experience_filters:
                if e == '0':        # 1년 미만
                    queries |= Q(experience__lt=1)
                elif e == '1':      # 1년 이상 ~ 3년 미만
                    queries |= Q(experience__gte=1, experience__lt=3)
                elif e == '3':      # 3년 이상 ~ 5년 미만
                    queries |= Q(experience__gte=3, experience__lt=5)
                elif e == '5':      # 5년 이상
                    queries |= Q(experience__gte=5)
            experts_qs = experts_qs.filter(queries)
        
        # 인증배지 필터링
        if badge_filter == 'true':
            experts_qs = experts_qs.filter(badge='VERIFIED')

        total_count = experts_qs.count()
        experts = list(experts_qs[:5]) if not show_all else list(experts_qs)


    # 인증된 전문가 중 랜덤 3명 추출
    verified_experts = Expert.objects.filter(badge=BadgeChoices.VERIFIED)
    recommended_experts = random.sample(list(verified_experts), min(3, verified_experts.count()))

    context = {
        'experts' : experts,
        'total_count': len(experts),
        'recommended_experts': recommended_experts,
        'keyword' : keyword,
        'selected_region' : region_filters,
        'selected_experience': experience_filters,
        'badge': badge_filter == 'true',
        'show_all' : show_all,
        'region_list' : [r[1] for r in RegionChoices.choices]  # 지역 필터를 한글 기준으로 전달
    }

    return render(request, 'experts/expert.html', context)

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