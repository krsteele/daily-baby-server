from django.db import models
from .photos import Photo
from cloudinary.models import CloudinaryField


class Baby(models.Model):

    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    nickname = models.CharField(max_length=25)
    birth_date = models.DateField(default="0000-00-00",)
    profile_image = CloudinaryField('profile_image')