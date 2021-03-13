from django.db import models

class DaysOfWeek(models.Model):

    day = models.CharField(max_length=20)
    