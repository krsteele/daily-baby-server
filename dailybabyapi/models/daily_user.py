from dailybabyapi.models.photos import Photo
from django.db import models

from django.contrib.auth.models import User
from .photos import Photo
from datetime import timezone



class DailyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text_time = models.TimeField(auto_now=False, auto_now_add=False)
    phone_number = models.CharField(max_length=15)
    profile_image = models.CharField(max_length=200)
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    