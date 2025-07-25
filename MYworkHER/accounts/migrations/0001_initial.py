# Generated by Django 4.2.21 on 2025-07-11 18:18

import accounts.models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(max_length=10, unique=True)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('region', models.CharField(choices=[('Gangnam-gu', '강남구'), ('Gangdong-gu', '강동구'), ('Gangbuk-gu', '강북구'), ('Gangseo-gu', '강서구'), ('Gwanak-gu', '관악구'), ('Gwangjin-gu', '광진구'), ('Guro-gu', '구로구'), ('Geumcheon-gu', '금천구'), ('Nowon-gu', '노원구'), ('Dobong-gu', '도봉구'), ('Dongdaemun-gu', '동대문구'), ('Dongjak-gu', '동작구'), ('Mapo-gu', '마포구'), ('Seodaemun-gu', '서대문구'), ('Seocho-gu', '서초구'), ('Seongdong-gu', '성동구'), ('Seongbuk-gu', '성북구'), ('Songpa-gu', '송파구'), ('Yangcheon-gu', '양천구'), ('Yeongdeungpo-gu', '영등포구'), ('Yongsan-gu', '용산구'), ('Eunpyeong-gu', '은평구'), ('Jongno-gu', '종로구'), ('Jung-gu', '중구'), ('Jungnang-gu', '중랑구')], max_length=20)),
                ('userType', models.CharField(choices=[('CUSTOMER', '고객'), ('EXPERT', '전문가'), ('ADMIN', '관리자')], default='CUSTOMER', max_length=10)),
                ('introduction', models.TextField(max_length=200)),
                ('idImage', models.ImageField(blank=True, null=True, upload_to=accounts.models.upload_image_path)),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to=accounts.models.upload_image_path)),
                ('isVerified', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
