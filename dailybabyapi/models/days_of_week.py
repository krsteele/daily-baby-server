from django.db import models

class DayOfWeek(models.Model):

    day = models.CharField(max_length=20)
