from django.core.management.base import BaseCommand, CommandError
from preston.crest import Preston
from cwo.models import Structure
from cwo.models import Alliance
from cwo.models import System
from cwo.models import Region
from cwo.models import Event
from django.utils import timezone
from decimal import *
import datetime
import pprint
import requests

class Command(BaseCommand):
    help = 'Update Sov Info'

    def handle(self, *args, **options):
        try:
            self.preston = Preston()
            self.today = timezone.now()
            self.end_of_time = datetime.datetime(9999, 12, 31, 23, 59, 59, tzinfo=self.today.tzinfo)

            alliances, current, current_hash, snapshot = self.preload()

            print('processing...')
            snapshot_hash = {}
            for s in snapshot.items:
                snapshot_hash[s.structureID] = s

                if s.alliance.id not in alliances:
                    self.add_aliance(s, alliances)

                if s.structureID in current_hash:
                    cs = current_hash[s.structureID]
                    defence = Decimal(s.vulnerabilityOccupancyLevel if 'vulnerabilityOccupancyLevel' in s.data else 0).quantize(Decimal('.1'))
                    if s.alliance.id != cs.alliance_id or defence != cs.defence:
                        db_system = System.objects.get(pk=s.solarSystem.id)
                        db_region = Region.objects.get(pk=db_system.region_id)
                        print('existing structure {} / {} changed A: {}>{}  D: {}>{}'.format(db_region.name, db_system.name, cs.alliance_id, s.alliance.id, cs.defence, defence))
                        cs.date2 = self.today
                        cs.save()
                        self.import_from_dict(s)
                        if defence == 0 and cs.defence != 0:
                            self.add_event(system_id=s.solarSystem.id, alliance_id=s.alliance.id, type_id=s.type.id, date=self.today, event_type='Reinforced', defence1=cs.defence, defence2=0)
                        if defence != 0 and cs.defence == 0:
                            self.add_event(system_id=s.solarSystem.id, alliance_id=s.alliance.id, type_id=s.type.id, date=self.today, event_type='Defended', defence1=0, defence2=defence)
                        if s.alliance.id != cs.alliance_id:
                            self.add_event(system_id=s.solarSystem.id, alliance_id=s.alliance.id, type_id=s.type.id, date=self.today, event_type='New Owner', defence1=cs.defence, defence2=defence)

                else:
                    db_system = System.objects.get(pk=s.solarSystem.id)
                    db_region = Region.objects.get(pk=db_system.region_id)
                    print('new structure {} / {}'.format(db_region.name, db_system.name))
                    self.import_from_dict(s)
                    self.add_event(system_id=s.solarSystem.id, alliance_id=s.alliance.id, type_id=s.type.id, date=self.today, event_type='New', defence1=0, defence2=0)
            print('done')

            self.delete_old(current, snapshot_hash)
        except requests.exceptions.ConnectionError:
            print('server offline')

    def add_event(self, system_id, alliance_id, type_id, date, event_type, defence1, defence2):
        db_system = System.objects.get(pk=system_id)
        db_alliance = Alliance.objects.get(pk=alliance_id)
        event = Event(
            system=db_system,
            alliance=db_alliance,
            type_id=type_id,
            date=date,
            event_type=event_type,
            defence1=defence1,
            defence2=defence2
        )
        event.save()

    def add_aliance(self, s, alliances):
        print('new alliance {}'.format(s.alliance.name))
        alliance = Alliance(id=s.alliance.id, name=s.alliance.name)
        alliance.save()
        alliances[s.alliance.id] = alliance

    def delete_old(self, current, snapshot_hash):
        print('deleting old...')
        for cs in current:
            if cs.structure_id not in snapshot_hash:
                db_system = System.objects.get(pk=cs.system_id)
                db_region = Region.objects.get(pk=db_system.region_id)
                print('lost structure {} / {}'.format(db_region.name, db_system.name))
                cs.date2 = self.today
                cs.save()
                self.add_event(system_id=cs.system_id, alliance_id=cs.alliance_id, type_id=cs.type_id, date=self.today, event_type='Lost', defence1=0, defence2=0)
        print('done')


    def preload(self):
        print('preloading...')
        alliances = {}
        for item in Alliance.objects.all():
            alliances[item.id] = item

        current = Structure.objects.filter(date1__lte=self.today, date2__gte=self.today)
        current_hash = {}
        for item in current:
            current_hash[item.structure_id] = item

        snapshot = self.preston.sovereignty.structures()
        print('done')

        return alliances, current, current_hash, snapshot



    def import_from_dict(self, structure):
        try:
            defence = structure.vulnerabilityOccupancyLevel if 'vulnerabilityOccupancyLevel' in structure.data else 0

            new = Structure(
                alliance_id=structure.alliance.id,
                defence=defence,
                structure_id=structure.structureID,
                system_id=structure.solarSystem.id,
                type_id=structure.type.id,
                date1=self.today,
                date2=self.end_of_time
            )
            new.save()
        except:
            pprint.pprint(structure.data)
            raise