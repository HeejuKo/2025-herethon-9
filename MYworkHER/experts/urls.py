from django.urls import path
from .views import *

app_name = 'experts'

urlpatterns = [
    path('', expert_list, name='expert_list'),                      # 필터 기반 전문가 전체 보기 (expert.html)
    path('search/', expert_search, name='expert_search'),                # 키워드 검색 결과 (expert_search.html)
    path('<int:expert_id>/', expert_detail, name='expert_detail'),       # 전문가 상세 페이지
]