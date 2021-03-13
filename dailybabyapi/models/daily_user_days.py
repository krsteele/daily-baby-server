from django.db import models

from .daily_user import DailyUser
from .days_of_week import DayOfWeek

class DailyUserDay(models.Model):
    user = models.ForeignKey("DailyUser", on_delete=models.CASCADE)
    day = models.ForeignKey("DayOfWeek", on_delete=models.CASCADE)
