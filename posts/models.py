from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    specialty = models.CharField(max_length=50, default=True)
    plan = models.PositiveIntegerField(default='0')
    plan_rez = models.PositiveIntegerField(default='0')
    plan_clock = models.PositiveIntegerField(default='0')
    plan_clock_rez = models.PositiveIntegerField(default='0')
    plan_all = models.PositiveIntegerField(default='0')
    plan_rez_all = models.PositiveIntegerField(default='0')
    plan_clock_all = models.PositiveIntegerField(default='0')
    plan_defect = models.PositiveIntegerField(default='0', blank=True)
    plan_defect_all = models.PositiveIntegerField(default='0')
    cex_plan_all = models.PositiveIntegerField(default='0')
    cex_defect_all = models.PositiveIntegerField(default='0')
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]
