from django.db import models


class Entry(models.Model):
    user_baby = models.ForeignKey("UserBaby", on_delete=models.CASCADE)
    prompt = models.ForeignKey("Prompt", on_delete=models.SET_NULL, null=True)
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    text = models.CharField(max_length=1500)
    is_private = models.BooleanField(default=None)
