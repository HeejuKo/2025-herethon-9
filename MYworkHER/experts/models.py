from django.utils import timezone
from django.db import models
from matching.models import Matching
from accounts.models import User

class CategoryChoices(models.TextChoices):
    APPLIANCE = 'APPLIANCE', '가전/수리'
    HEALTH = 'HEALTH', '헬스/스포츠'
    BUSINESS = 'BUSINESS', '컨설팅/비지니스'
    LIFESTYLE = 'LIFESTYLE', '생활/라이프'

class BadgeChoices(models.TextChoices):
    NONE = '', '없음'
    VERIFIED = 'VERIFIED', '인증배지'

class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile')
    category = models.CharField(max_length=20, choices=CategoryChoices.choices, null=False)
    bio = models.TextField(max_length=200)
    description = models.TextField()            # 업무 상세 설명
    experience = models.IntegerField()          # 경력 (단위 : 년)
    badge = models.CharField(max_length=20, choices=BadgeChoices.choices, default=BadgeChoices.NONE)

    # 한 달 예약 수
    @property
    def monthly_matching_count(self):
        today = timezone.now()
        return Matching.objects.filter(
            expert = self.user,
            status = 'COMPLETE',
            date__year = today.year,
            date__month = today.month
        ).count()

    def __str__(self):
        return f'{self.user.nickname} - {self.category}'