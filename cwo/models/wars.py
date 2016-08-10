from django.db import models

from cwo.models import Region
from cwo.models import Alliance
from cwo.models import System
import random




class War(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    date1 = models.DateTimeField(null=True)
    date2 = models.DateTimeField(null=True)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)

    def info(self):
        return {
            'name': self.name,
            'participants': [p.info() for p in self.participant_set.all()],
            'territories': [t.info() for t in self.territory_set.all()]
        }


class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    war = models.ForeignKey(War, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=7, null=True)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)

    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'alliances': [pa.info() for pa in self.participantalliance_set.all()]
        }

    def data(self):
        return [
            {'date': 'Date.UTC(1970, 10, 4)', 'value': random.random()*100 },
            {'date': 'Date.UTC(1970, 10, 5)', 'value': random.random()*100 },
            {'date': 'Date.UTC(1970, 10, 7)', 'value': random.random()*100 },
            {'date': 'Date.UTC(1970, 10, 10)', 'value': random.random()*100 },
            {'date': 'Date.UTC(1970, 10, 20)', 'value': random.random()*100 },
        ]


class ParticipantAlliance(models.Model):
    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, null=True)
    alliance = models.ForeignKey(Alliance, on_delete=models.CASCADE, null=True)
    date1 = models.DateTimeField()
    date2 = models.DateTimeField()

    def __str__(self):
        return "[{}]".format(self.id)

    def info(self):
        return {
            'id': self.id,
            'alliance_id': self.alliance_id,
            'alliance_name': self.alliance.name,
            'date1': self.date1.strftime ('%Y-%m-%d %H:%M:%S'),
            'date2': self.date2.strftime ('%Y-%m-%d %H:%M:%S')
        }


class Territory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    war = models.ForeignKey(War, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)

    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'regions': [tr.info() for tr in self.territoryregion_set.all()]
        }


class TerritoryRegion(models.Model):
    id = models.AutoField(primary_key=True)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "[{}]".format(self.id)

    def info(self):
        return {
            'id': self.id,
            'region_id': self.region_id,
            'region_name': self.region.name
        }

