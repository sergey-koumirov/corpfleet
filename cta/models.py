from django.db import models

class RawData(models.Model):
    raw = models.TextField()
    date = models.DateTimeField()
    name = models.CharField(max_length = 200)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)