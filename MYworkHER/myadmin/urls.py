from django.urls import path
from .views import *

app_name = 'myadmin'

urlpatterns = [
    path('', user_list, name='user_list'),
    path('user/<int:user_id>', user_detail, name='user_detail'),
]