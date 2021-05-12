from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User




class DailyUser(models.Model):

    def days_default():
        return [0, 0, 0, 0, 0, 0, 0]
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text_time = models.TimeField(auto_now=False, auto_now_add=False)
    phone_number = models.CharField(max_length=15)
    profile_image = models.CharField(max_length=200)
    days_of_week = ArrayField(models.IntegerField(), size=7, default=days_default)
    