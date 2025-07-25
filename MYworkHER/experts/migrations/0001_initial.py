# Generated by Django 4.2.21 on 2025-07-11 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('APPLIANCE', '가전/수리'), ('HEALTH', '헬스/스포츠'), ('BUSINESS', '컨설팅/비지니스'), ('LIFESTYLE', '생활/라이프')], max_length=20)),
                ('bio', models.TextField(max_length=200)),
                ('description', models.TextField()),
                ('experience', models.IntegerField()),
                ('badge', models.CharField(choices=[('', '없음'), ('VERIFIED', '인증배지')], default='', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='expert_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
