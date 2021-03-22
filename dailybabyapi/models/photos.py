from django.db import models

class Photo(models.Model):
    image = models.CharField(max_length=200)
    entry = models.ForeignKey("Entry", on_delete=models.CASCADE)
