from django.db import models

class Relationship(models.Model):

    type = models.CharField(max_length=50)