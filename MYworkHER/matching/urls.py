from django.urls import path
from .views import *

app_name = 'matching'

urlpatterns = [
    path('create/', create_matching, name='create-matching'),
    path('', main, name='main'),
    path('<int:matching_id>/', matching_detail, name='reserve-confirm'),        # 예약 확인
    path('<int:matching_id>/edit/', edit_matching, name='edit-matching'),        # 예약 수정 (matching.html 사용)
    path('<int:matching_id>/', matching_success, name='matching_success'),
    path('submit/', submit_reservation, name='submit_reservation'),
]