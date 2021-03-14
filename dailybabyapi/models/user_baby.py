from django.db import models


class UserBaby(models.Model):
    user = models.ForeignKey("DailyUser", on_delete=models.CASCADE)
    baby = models.ForeignKey("Baby", on_delete=models.CASCADE)
    relationship = models.ForeignKey("Relationship", on_delete=models.PROTECT)
    
