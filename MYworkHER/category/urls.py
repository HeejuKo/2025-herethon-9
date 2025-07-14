from django.urls import path
from .views import *

app_name = 'category'

urlpatterns = [
    path('', category_list, name='category_list'),                       # 카테고리 메인 (category.html)
    path('search/', expert_category, name='expert_category'),          # 카테고리 기반 필터링 (category_expert.html)
]