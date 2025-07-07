from django.urls import path
from .views import *

app_name = 'matching'

urlpatterns = [
    path('', create_matching, name='create-matching'),
    path('main', main, name='main'),
    path('success/', matching_success, name='matching-success'),
]