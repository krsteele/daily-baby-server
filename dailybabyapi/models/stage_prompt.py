from django.db import models


class StagePrompt(models.Model):
    stage = models.ForeignKey("Stage", on_delete=models.CASCADE)
    prompt = models.ForeignKey("Prompt", on_delete=models.CASCADE)