from django.db import models
from .photos import Photo
from cloudinary.models import CloudinaryField


class Baby(models.Model):

    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    nickname = models.CharField(max_length=25)
    birth_date = models.DateField(default="0000-00-00",)
    profile_image = CloudinaryField('profile_image', default="https://res.cloudinary.com/fluffydaydream/image/upload/w_1000,c_fill,ar_1:1,g_auto,r_max,b_rgb:262c35/v1615834269/blank-profile-picture-973460_640_rtmmdv.png")