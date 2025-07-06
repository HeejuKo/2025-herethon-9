from django.urls import path
from .views import *

app_name = 'acoounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', mypage, name='mypage'),
]