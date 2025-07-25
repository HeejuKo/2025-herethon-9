# Generated by Django 4.2.21 on 2025-07-14 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='subcategory',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='expert',
            name='badge',
            field=models.CharField(blank=True, choices=[('', '없음'), ('VERIFIED', '인증배지')], default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='expert',
            name='bio',
            field=models.TextField(default='자기소개를 적어주세요.', max_length=200),
        ),
        migrations.AlterField(
            model_name='expert',
            name='category',
            field=models.CharField(choices=[('APPLIANCE', '가전/수리'), ('HEALTH', '헬스/스포츠'), ('BUSINESS', '컨설팅/비지니스'), ('LIFESTYLE', '생활/라이프')], default='APPLIANCE', max_length=20),
        ),
        migrations.AlterField(
            model_name='expert',
            name='description',
            field=models.TextField(default='업무 상세 설명을 적어주세요.'),
        ),
        migrations.AlterField(
            model_name='expert',
            name='experience',
            field=models.IntegerField(default=0),
        ),
    ]
