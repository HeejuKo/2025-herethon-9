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
def expert_category(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')

    region_filters = request.GET.getlist('region')
    experience_filters = request.GET.getlist('experience')
    badge_filter = request.GET.get('badge')
    seoul_all = request.GET.get('seoul_all') == 'true'
    show_all = request.GET.get('show_all') == 'true'

    category_value = None
    category_label = None
    experts_qs = Expert.objects.select_related('user').all()

    # 카테고리 및 서브카테고리 필터
    if category in CATEGORY_ENUM_MAP:
        category_value, category_label = CATEGORY_ENUM_MAP[category]
        experts_qs = experts_qs.filter(category=category_value)

        if subcategory:
            experts_qs = experts_qs.filter(subcategory=subcategory)

    # 필터 적용
    experts_qs = apply_region_filter(experts_qs, region_filters, seoul_all)
    experts_qs = apply_experience_filter(experts_qs, experience_filters)
    experts_qs = apply_badge_filter(experts_qs, badge_filter)

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