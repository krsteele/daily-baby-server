from dailybabyapi.models.photos import Photo
from django.db import models

from django.contrib.auth.models import User
from .photos import Photo
from datetime import timezone
from cloudinary.models import CloudinaryField



class DailyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    phone_number = models.CharField(max_length=15)
    profile_image = CloudinaryField('profile_image', default="https://res.cloudinary.com/fluffydaydream/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,b_rgb:262c35/v1615834269/blank-profile-picture-973460_640_rtmmdv.png")
    