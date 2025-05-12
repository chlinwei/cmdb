from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('developer_supremo', '总监'),
        ('developer_manager', '经理'),
        ('developer', '研发'),
    )
    role = models.CharField(max_length=32, choices=ROLES, default='developer')
    remark = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-id']

    def __str__(self):
        return self.username