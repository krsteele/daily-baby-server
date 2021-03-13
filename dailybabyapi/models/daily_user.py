from django.db import models

from django.contrib.auth.models import User


class DailyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_pics", max_length=None, width_field=None, height_field=None)
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=None)
    bio = models.CharField(max_length=50)