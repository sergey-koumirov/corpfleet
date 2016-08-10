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
    system_id = models.BigIntegerField(db_index=True)
    type_id = models.BigIntegerField()
    date1 = models.DateTimeField()
    date2 = models.DateTimeField()

    def __str__(self):
        return "[{}]".format(self.id)

