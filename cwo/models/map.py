from django.db import models

class System(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    region_id = models.BigIntegerField()
    constellation_id = models.BigIntegerField()
    security_status = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)


class Constellation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    region_id = models.BigIntegerField()

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)


class Region(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)