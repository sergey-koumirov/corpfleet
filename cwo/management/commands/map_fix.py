from django.core.management.base import BaseCommand, CommandError
from cwo.models import System
from cwo.models import Region
import sys
from cwo.common import Vector
from math import sqrt

class Command(BaseCommand):
    help = 'Fix Map Info'
    factor = 4

    def handle(self, *args, **options):
        print('processing...')
        for region in Region.objects.filter(name='Geminate'):
            print(region.name)
            db_systems = System.objects.filter(region_id=region.id)
            (min_x, max_x, min_z, max_z, dist) = self.minmaxdist(db_systems)
            print(dist)

            systems = {}
            for s in db_systems:
                systems[s.id]={'name': s.name, 'id': s.id, 'x': s.x, 'z': s.z}

            while True:
                cnt = 0
                new = {}
                for key1, s1 in systems.items():
                    v1 = Vector(s1['x'], s1['z'])
                    near = []
                    for key2, s2 in systems.items():
                        if s2['id'] != s1['id']:
                            v2 = Vector(s2['x'], s2['z'])
                            if self.is_near(v1,v2,dist):
                                cnt += 1
                                near.append(s2)
                                print(
                                    s1['name'],
                                    s2['name'],
                                    '{:,.2f}'.format( (v1-v2).norm() ),
                                    '{:,.2f}'.format( dist ),
                                    '{:,.2f}'.format( v1.values[0]),
                                    '{:,.2f}'.format( v1.values[1])
                                )
                    if len(near)>0:
                        vn = Vector(0,0)
                        for n in near:
                            v2 = Vector(n['x'], n['z'])
                            x = v2.values[0]
                            y = v2.values[1]
                            vn += (v1 - v2) * (dist / (sqrt((x / self.factor) * (x / self.factor) + y * y)))
                        vn = v1 + vn * (1.0 / len(near))
                        new[s1['id']] = [vn.values[0], vn.values[1]]
                        print('Diff: ', '{:,.2f}'.format(vn.values[0]), '{:,.2f}'.format(vn.values[1]))

                print('--------------------------------------------------------')
                if cnt==0:
                    break
                else:
                    for key, n in new.items():
                        systems[key]['x'] = n[0]
                        systems[key]['z'] = n[1]

            for key, s in systems.items():
                print(s)
                record=System.objects.get(id=s['id'])
                record.ax = s['x']
                record.ay = record.y
                record.az = s['z']
                record.save()


    def is_near(self, v1, v2, dist):
        v = v1-v2
        x = v.values[0]
        y = v.values[1]
        return (1/(self.factor*self.factor))*x*x + y*y <= dist*dist

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
        dist = max(max_x-min_x, max_z-min_z) / 50.0
        return (min_x, max_x, min_z, max_z, dist)





