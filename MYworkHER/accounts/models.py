from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from uuid import uuid4

class UserType(models.TextChoices):
    CUSTOMER = 'CUSTOMER', '고객'
    EXPERT = 'EXPERT', '전문가'

class RegionChoices(models.TextChoices):
    GANGNAM = 'Gangnam-gu', '강남구'
    GANGDONG = 'Gangdong-gu', '강동구'
    GANGBUK = 'Gangbuk-gu', '강북구'
    GANGSEO = 'Gangseo-gu', '강서구'
    GWANAK = 'Gwanak-gu', '관악구'
    GWANGJIN = 'Gwangjin-gu', '광진구'
    GURO = 'Guro-gu', '구로구'
    GEUMCHEON = 'Geumcheon-gu', '금천구'
    NOWON = 'Nowon-gu', '노원구'
    DOBONG = 'Dobong-gu', '도봉구'
    DONGDAEMUN = 'Dongdaemun-gu', '동대문구'
    DONGJAK = 'Dongjak-gu', '동작구'
    MAPO = 'Mapo-gu', '마포구'
    SEODAEMUN = 'Seodaemun-gu', '서대문구'
    SEOCHO = 'Seocho-gu', '서초구'
    SEONGDONG = 'Seongdong-gu', '성동구'
    SEONGBUK = 'Seongbuk-gu', '성북구'
    SONGPA = 'Songpa-gu', '송파구'
    YANGCHEON = 'Yangcheon-gu', '양천구'
    YEONGDEUNGPO = 'Yeongdeungpo-gu', '영등포구'
    YONGSAN = 'Yongsan-gu', '용산구'
    EUNPYEONG = 'Eunpyeong-gu', '은평구'
    JONGNO = 'Jongno-gu', '종로구'
    JUNG = 'Jung-gu', '중구'
    JUNGRANG = 'Jungnang-gu', '중랑구'

def upload_image_path(instance, filename):
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{instance.username}/{uuid4().hex}_{file_basename}'

class User(AbstractUser):
    nickname = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    region = models.CharField(max_length=20, choices=RegionChoices.choices, blank=False, null=False)
    userType = models.CharField(max_length=10, choices=UserType.choices, default=UserType.CUSTOMER)
    introduction = models.TextField(max_length=200)
    idImage = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    profileImage = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    isVerified = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} {self.nickname}'