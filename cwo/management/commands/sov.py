from django.core.management.base import BaseCommand, CommandError
from preston.crest import Preston
from cwo.models import Structure
from cwo.models import Alliance
from django.utils import timezone
from decimal import *
import datetime
import pprint

class Command(BaseCommand):
    help = 'Update Sov Info'

    def handle(self, *args, **options):
        preston = Preston()
        today = timezone.now()
        end_of_time = datetime.datetime(9999, 12, 31, 23, 59, 59, tzinfo=today.tzinfo)
        print(today)

        alliances = {}
        for item in Alliance.objects.all():
            alliances[item.id] = item
        print('alliances loaded')

        current = Structure.objects.filter(date1__lte=today, date2__gte=today)
        current_hash = {}
        for item in current:
            current_hash[item.structure_id] = item
        print('current state loaded')

        snapshot = preston.sovereignty.structures()
        print('new state loaded')

        snapshot_hash = {}
        for s in snapshot.items:
            snapshot_hash[s.structureID] = s

            if s.alliance.id not in alliances:
                alliance = Alliance(id=s.alliance.id, name=s.alliance.name)
                alliance.save()

            if s.structureID in current_hash:
                cs = current_hash[s.structureID]
                defence = Decimal(s.vulnerabilityOccupancyLevel if 'vulnerabilityOccupancyLevel' in s.data else 0).quantize(Decimal('.01'))
                if s.alliance.id != cs.alliance_id or defence != cs.defence:
                    print('existing structure changed A: {}>{}  D: {}>{}'.format(s.alliance.id, cs.alliance_id, defence, cs.defence))
                    cs.date2 = today
                    cs.save()
                    Structure.import_from_dict(today, end_of_time, s)
            else:
                print('new structure')
                Structure.import_from_dict(today, end_of_time, s)

        print('deleting old')

        for cs in current:
            if cs.structure_id not in snapshot_hash:
                print('lost structure')
                cs.date2 = today
                cs.save()

        print('finished')
