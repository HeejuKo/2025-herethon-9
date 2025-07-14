from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/step1/', signup_step1, name='signup_step1'),
    path('signup/step2/', signup_step2, name='signup_step2'),
    path('signup/step3/', signup_step3, name='signup_step3'),
    path('signup/step4/', signup_step4, name='signup_step4'),
    path('signup/step5/', signup_step5, name='signup_step5'),
    path('signup/step6/', signup_step6, name='signup_step6'),
    path('signup/step7/', signup_step7, name='signup_step7'),
    path('signup/complete/', signup_complete, name='signup_complete'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', mypage, name='mypage'),
    path('mypage-update/', mypage_update, name='mypage_update'),
]