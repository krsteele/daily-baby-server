from django.db import models

class Stage(models.Model):

    stage = models.CharField(max_length=25)
    