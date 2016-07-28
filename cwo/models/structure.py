from django.db import models
import pprint

class StructureType(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)

class Structure(models.Model):
    id = models.AutoField(primary_key=True)
    alliance_id = models.BigIntegerField()
    defence = models.DecimalField(max_digits=5, decimal_places=2)
    structure_id = models.BigIntegerField()
    system_id = models.BigIntegerField()
    type_id = models.BigIntegerField()
    date1 = models.DateTimeField()
    date2 = models.DateTimeField()

    def import_from_dict(today, end_of_time, structure):
        try:
            defence = structure.vulnerabilityOccupancyLevel if 'vulnerabilityOccupancyLevel' in structure.data else 0

            new = Structure(
                alliance_id=structure.alliance.id,
                defence=defence,
                structure_id=structure.structureID,
                system_id=structure.solarSystem.id,
                type_id=structure.type.id,
                date1=today,
                date2=end_of_time
            )
            new.save()
        except:
            pprint.pprint(structure.data)
            pprint.pprint(type(structure.data))
            pprint.pprint('vulnerabilityOccupancyLevel' in structure.data)
            pprint.pprint('alliance' in structure.data)
            raise

    def __str__(self):
        return "[{}]".format(self.id)

