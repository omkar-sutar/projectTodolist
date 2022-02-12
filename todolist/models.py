from django.db import models

# Create your models here.

class Tasks(models.Model):
    username=models.CharField(max_length=64,primary_key=True)
    tasks=models.JSONField(blank=True)