from django.urls import path
from .views import *

app_name = 'experts'

urlpatterns = [
    path('', category_list, name='category_list'),                       # 카테고리 메인 (category.html)
    path('category/', expert_category, name='expert_category'),          # 카테고리 기반 필터링 (category_expert.html)
    path('list/', expert_list, name='expert_list'),                      # 필터 기반 전문가 전체 보기 (expert.html)
    path('search/', expert_search, name='expert_search'),                # 키워드 검색 결과 (expert_search.html)
    path('<int:expert_id>/', expert_detail, name='expert_detail'),       # 전문가 상세페이지
]