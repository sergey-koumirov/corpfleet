from django.db import models

class RawData(models.Model):
    raw = models.TextField()
    date = models.DateTimeField()
    name = models.CharField()