from django.db import models
from django.utils import timezone

from accounts.models import User

class Matching(models.Model):
    STATUS_CHOICES = [
        ('PENDING' , '대기 중'),
        ('REJECTED', '거절'),
        ('COMPLETE', '완료'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_matching')
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expert_matching')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"예약 {self.pk} - 고객 {self.customer_id} → 전문가 {self.expert_id}"