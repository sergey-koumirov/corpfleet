from django.core.management.base import BaseCommand, CommandError
from preston.crest import Preston
from cwo.models import Region
from cwo.models import Constellation
from cwo.models import System
from cwo.models import Gate

import pprint


class Command(BaseCommand):
    help = 'Create Map Records'

    def handle(self, *args, **options):
        preston = Preston()
        regions = preston.regions()
        for region in regions.items:
            r, created = Region.objects.get_or_create(id=region.id, name=region.name)
            r.save()
            for constellation in region().constellations:
                constellation_info = constellation()
                c, created = Constellation.objects.get_or_create(
                    id=constellation.id,
                    name=constellation_info.name,
                    region_id=region.id
                )
                c.save()

                for system in constellation_info.systems:
                    system_info = system()
                    print(system_info.name)
                    s, created = System.objects.get_or_create(
                        id=system.id,
                        name=system_info.name,
                        region_id=region.id,
                        constellation_id=constellation.id,
                        security_status=system_info.securityStatus,
                        x=system_info.position.x,
                        y=system_info.position.y,
                        z=system_info.position.z
                    )
                    s.save()

                    # print(system_info)
                    # print(system_info.stargates)

                    for gate in system_info.stargates:
                        print(gate.name)
                        gate_info = gate()
                        g, created = Gate.objects.get_or_create(
                            id=gate.id,
                            system_from_id=system.id,
                            system_to_id=gate_info.destination.system.id
                        )
                        s.save()




