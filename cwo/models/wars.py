from django.db import models
from django.db import connection
from cwo.models import Region
from cwo.models import Alliance
from cwo.models import System


class War(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)

    def info(self):
        return {
            'name': self.name,
            'participants': [p.info() for p in self.participant_set.all()],
            'territories': [t.info() for t in self.territory_set.all()]
        }

    def systems(self):

        mm = self.minmax()

        result = []
        sql = (
            'SELECT s.* '
            '  FROM cwo_dev.cwo_system s '
            '  where s.region_id in ('
            '          select tr.region_id '
            '            from cwo_dev.cwo_territoryregion tr, cwo_dev.cwo_territory t '
            '            where tr.territory_id = t.id '
            '              and t.war_id = %s'
            '        )'
        )
        for s in System.objects.raw(sql, [self.id]):
            result.append({
                'name': s.name,
                'sx': (s.x - mm['minx']) / mm['factor'],
                'sy': (s.y - mm['miny']) / mm['factor'],
                'sz': 1000-(s.z - mm['minz']) / mm['factor'],
            })
        return result

    def minmax(self):
        sql = (
            'SELECT min(s.x) as minx, max(s.x) as maxx, '
            '       min(s.y) as miny, max(s.y) as maxy, '
            '       min(s.z) as minz, max(s.z) as maxz '
            '  FROM cwo_dev.cwo_system s '
            '  where s.region_id in ('
            '          select tr.region_id '
            '            from cwo_dev.cwo_territoryregion tr, cwo_dev.cwo_territory t '
            '            where tr.territory_id = t.id '
            '              and t.war_id = %s'
            '        )'
        )
        cursor = connection.cursor()
        cursor.execute(sql, [self.id])
        result = cursor.fetchone()
        return {
            'minx': result[0],
            'maxx': result[1],
            'miny': result[2],
            'maxy': result[3],
            'minz': result[4],
            'maxz': result[5],
            'width': result[1]-result[0],
            'height': result[3]-result[2],
            'deep': result[5]-result[4],
            'factor': max(result[1]-result[0],result[5]-result[5]) / 1000
        }

    def statistics(self):
        return {
            'systems': self.systems(),
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

