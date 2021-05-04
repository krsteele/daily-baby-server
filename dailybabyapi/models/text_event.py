# blueprint for a text event
from django.db import models


class TextEvent(models.Model):
    user = models.ForeignKey("DailyUser", on_delete=models.CASCADE)
    message_body = models.CharField(max_length=140)
    phone_number = models.CharField(max_length=15)
    execution_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=15)







# user_name???
# timezone???
# task_id???