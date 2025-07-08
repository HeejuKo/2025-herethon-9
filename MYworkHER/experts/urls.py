from django.urls import path
from .views import *

app_name = 'experts'

urlpatterns = [
    path('', expert_list, name='expert_list'),
    path('<int:expert_id>/', expert_detail, name='expert_detail'),
]