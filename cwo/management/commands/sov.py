from django.core.management.base import BaseCommand, CommandError
from preston.crest import Preston
from cwo.models import Structure
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = 'Update Sov Info'

    def handle(self, *args, **options):
        preston = Preston()
        today = timezone.now()
        print(today)

        current = Structure.objects.filter(date1__lte=today, date2__gte=today)
        current_hash = {}
        for key, value in current.items():
            current_hash[key] = value

        snapshot = preston.sovereignty.structures()

        for structure in snapshot.items:

            if current_hash.has_key(structure.structureID):
                print('existing structure')
                str = Structure.objects.get(structure_id=structure.structureID)

            else:
                print('new structure')
                new = Structure(
                    alliance_id = structure.alliance.id,
                    defence = structure.vulnerabilityOccupancyLevel,
                    structure_id = structure.structureID,
                    system_id = structure.solarSystem.id,
                    type_id = structure.type.id,
                    date1 = today,
                    date2 = datetime.datetime(9999, 12, 31, 23, 59, 59)
                )
                new.save()
