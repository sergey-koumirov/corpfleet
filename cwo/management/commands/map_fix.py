from django.core.management.base import BaseCommand, CommandError
from cwo.models import System
from cwo.models import Region
import sys
from cwo.common import Vector

class Command(BaseCommand):
    help = 'Fix Map Info'

    def handle(self, *args, **options):
        print('processing...')
        for region in Region.objects.all():
            print(region.name)
            systems = System.objects.filter(region_id=region.id)
            (min_x, max_x, min_z, max_z, dist) = self.minmaxdist(systems)
            for s1 in systems:
                print(s1.name)
                while True:
                    cnt = 0
                    for s2 in systems:
                        v1 = Vector(3, 4)
                        print( v1.norm() )


                    if cnt==0:
                        break


            print(min_x, max_x, min_z, max_z, dist)

    def minmaxdist(self, systems):
        max_x = -sys.float_info.max
        min_x = sys.float_info.max
        max_z = -sys.float_info.max
        min_z = sys.float_info.max
        for system in systems:
            if max_x < system.x:
                max_x = system.x
            if max_z < system.z:
                max_z = system.z
            if min_x > system.x:
                min_x = system.x
            if min_z > system.z:
                min_z = system.z

        dist = max(max_x-min_x, max_z-min_z)

        return (min_x, max_x, min_z, max_z, dist)





