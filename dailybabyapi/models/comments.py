from django.db import models

class Comment(models.Model):
    entry = models.ForeignKey("Entry", on_delete=models.CASCADE)
    user = models.ForeignKey("DailyUser", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    content = models.CharField(max_length=500)