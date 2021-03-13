from django.db import models

class DailyUserDay(models.Model):
    user = models.ForeignKey("DailyUser", on_delete=models.CASCADE)
    day = models.ForeignKey("DayOfWeek", on_delete=models.CASCADE)
