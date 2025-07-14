from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from category.constants import CATEGORY_CHOICES

from accounts.models import *
from experts.models import *
from .models import *

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

def category_list(request):
    return render(request, 'category/category.html')  # 상위 카테고리 클릭 페이지

def category_list(request):
    category_enum_map = {
        'appliance': ('가전/수리', CategoryChoices.APPLIANCE, [
            '조명˙전등 수리', '가구 조립 및 수리', '방충망·창문 보수', '욕실 타일 보수', '도어락 교체',
            '에어컨 설치 및 수리', 'TV˙가전 설치 및 수리', '문 손잡이˙경첩 수리', '수도꼭지/샤워기 수리'
            ]),
        'health': ('헬스/스포츠', CategoryChoices.HEALTH, [
            '다이어트 코칭', '운동˙식단관리 코칭', '등산˙러닝˙사이클', '복싱˙격투기',
            '산전˙산후 운동', '체형˙거북목 교정', '필라테스˙요가', '수영˙아쿠아로빅˙다이빙'
            ]),
        'business': ('컨설팅/비즈니스', CategoryChoices.BUSINESS, [
            '여성 창업 컨설팅', '이력서˙자기소개서 코칭', '여성 CEO 멘토링', '워킹맘 멘토링',
            '경력단절여성 컨설팅', 'SNS 브랜딩 및 운영', '여성 리더십˙자기계발', '여성 프리랜서 멘토링'
            ]),
        'lifestyle': ('생활/라이프', CategoryChoices.LIFESTYLE, [
            '인테리어˙셀프시공', '반려동물 케어˙펫시터', '홈카페˙베이킹', '호신술˙경호술',
            '방문청소˙정리', '육아˙베이비시터', '요리˙살림˙자취'
            ]),
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

    return render(request, 'category/category.html', {'categories': categories})

@login_required
def expert_category(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')

    region_filters = request.GET.getlist('region')
    experience_filters = request.GET.getlist('experience')
    badge_filter = request.GET.get('badge')
    show_all = request.GET.get('show_all') == 'true'
    seoul_all = request.GET.get('seoul_all') == 'true'

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

    # 지역 필터링
    if region_filters and not seoul_all:
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
    if badge_filter == 'false':
        experts_qs = experts_qs.filter(badge=BadgeChoices.VERIFIED)

    total_count = experts_qs.count()
    experts = list(experts_qs[:10]) if not show_all else list(experts_qs)

    return render(request, 'category/category_expert.html', {
        'experts': experts,
        'total_count': total_count,
        'category_label': category_label,
        'subcategory_label': subcategory,
        'selected_region': region_filters,
        'selected_experience': experience_filters,
        'badge': badge_filter == 'true',
        'show_all': show_all,
        'seoul_all': seoul_all,
        'region_list': [r[1] for r in RegionChoices.choices],
    })