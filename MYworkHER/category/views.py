from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from category.constants import *
from accounts.models import *
from experts.models import *
from .models import *

def category_list(request):
    categories = {}

    for key, (enum_value, label) in CATEGORY_ENUM_MAP.items():
        sub_list = CATEGORY_CHOICES[enum_value]['subcategories']  # enum_value는 CategoryChoices.APPLIANCE 등

        subcategories = []
        for sub in sub_list:
            count = Expert.objects.filter(category=enum_value, subcategory=sub).count()
            subcategories.append({'name': sub, 'count': count})

        categories[key] = {
            'label': label,
            'subcategories': subcategories
        }

    return render(request, 'category/category.html', {'categories': categories})

# 지역구 필터링 영문 매핑
def get_region_value_by_label(label):
    for value, display in RegionChoices.choices:
        if label == display:  # 예: '마포구' == '마포구'
            return value       # 반환: 'MAPO'
    return None

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

        if subcategory:
            experts_qs = experts_qs.filter(subcategory=subcategory)

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