from django.db import models

class Prompt(models.Model):

    prompt = models.CharField(max_length=140)