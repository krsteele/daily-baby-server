from dailybabyapi.models.photos import Photo
from django.db import models

from django.contrib.auth.models import User


class DailyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text_time = models.TimeField(auto_now=False, auto_now_add=False, default=timezone.now)
    phone_number = models.CharField(max_length=15)
    profile_image = models.ForeignKey(Photo, on_delete=models.DO_NOTHING, null=True)
    