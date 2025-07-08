from django.shortcuts import render, get_object_or_404
from .models import Expert

def expert_detail(request, expert_id):
    expert = get_object_or_404(Expert, pk=expert_id)

    context = {
        'expert': expert,
        'nickname' : expert.user.nickname,
        'category_display' : expert.get_category_display(),

        'bio' : expert.bio,
        'description' : expert.description,

        'region' : expert.user.region,
        'experience' : expert.experience,
        'badge_display' : expert.get_badge_display(),
        'is_verified' : expert.badge == 'VERIFIED',

        'monthly_reservation' : expert.monthly_matching_count,
    }

    return render(request, 'experts/expert_detail.html', context)