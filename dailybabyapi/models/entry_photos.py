from django.db import models


class EntryPhoto(models.Model):
    entry = models.ForeignKey("Entry", on_delete=models.CASCADE)
    photo = models.ForeignKey("Photo", on_delete=models.CASCADE)