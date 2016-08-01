from django.db import models


class War(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)


class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    war_id = models.BigIntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)


class ParticipantAlliance(models.Model):
    id = models.AutoField(primary_key=True)
    participant_id = models.BigIntegerField()
    alliance_id = models.BigIntegerField()
    date1 = models.DateTimeField()
    date2 = models.DateTimeField()

    def __str__(self):
        return "[{}]".format(self.id)


class Territory(models.Model):
    id = models.AutoField(primary_key=True)
    war_id = models.BigIntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)


class TerritoryRegion(models.Model):
    id = models.AutoField(primary_key=True)
    territory_id = models.BigIntegerField()
    region_id = models.BigIntegerField()

    def __str__(self):
        return "[{}]".format(self.id)