"""
URL configuration for MYworkHER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from matching.views import main

urlpatterns = [
    path('', main, name='name'),
    path('admin/', admin.site.urls),
    path('matching/', include('matching.urls')),
    path('category/', include('category.urls')),
    path('experts/', include('experts.urls')),
    path('accounts/', include('accounts.urls')),
    path('chats/', include('chats.urls')),
    path('secret-admin/', include('myadmin.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # 이미지 업로드를 위한 설정 추가