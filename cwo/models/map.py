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

    ax = models.FloatField(null=True)
    ay = models.FloatField(null=True)
    az = models.FloatField(null=True)

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


class Gate(models.Model):
    id = models.BigIntegerField(primary_key=True)
    system_from_id = models.BigIntegerField()
    system_to_id = models.BigIntegerField()

    def __str__(self):
        return "[{}]".format(self.id)