from django.urls import path
from .views import *

app_name = 'experts'

urlpatterns = [
    path('', category_list, name='category_list'),              # 카테고리
    path('category/', expert_category, name='expert_category'),       # expert.html (카테고리 필터 결과)
    path('search', expert_list, name='expert_list'),                   # 전문가 검색 및 필터링
    path('<int:expert_id>/', expert_detail, name='expert_detail'),      # 전문가 상세페이지
]