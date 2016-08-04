from cwo.models import System
from cwo.models import Structure
from django.db import connection
import datetime

class WarMap:

    def __init__(self, war):
        self.war = war
        self.minmax = self.minmax()
        self.ownership = self.ownership()
        self.war_systems = self.war_systems()
        self.systems = self.systems()
        self.war_system_links = self.war_system_links()

    def map_info(self):
        return {
            'systems' : self.war_systems,
            'links': self.war_system_links
        }

    def war_systems(self):
        result = {}
        sql = (
            'SELECT s.* '
            '  FROM cwo_system s '
            '  where s.region_id in ('
            '          select tr.region_id '
            '            from cwo_territoryregion tr, cwo_territory t '
            '            where tr.territory_id = t.id '
            '              and t.war_id = %s'
            '        )'
        )
        for s in System.objects.raw(sql, [self.war.id]):
            result[s.id]={
                'name': s.name,
                'sx': (s.x - self.minmax['minx']) / self.minmax['factor'],
                'sy': (s.y - self.minmax['miny']) / self.minmax['factor'],
                'sz': 1000-(s.z - self.minmax['minz']) / self.minmax['factor'],
                'owners': self.ownership.get(s.id,[])
            }
        return result

    def systems(self):
        result = {}
        for s in System.objects.raw('SELECT s.* FROM cwo_system s '):
            result[s.id]={
                'name': s.name,
                'sx': (s.x - self.minmax['minx']) / self.minmax['factor'],
                'sy': (s.y - self.minmax['miny']) / self.minmax['factor'],
                'sz': 1000-(s.z - self.minmax['minz']) / self.minmax['factor'],
                'owners': self.ownership.get(s.id,[])
            }
        return result

    def minmax(self):
        sql = (
            'SELECT min(s.x) as minx, max(s.x) as maxx, '
            '       min(s.y) as miny, max(s.y) as maxy, '
            '       min(s.z) as minz, max(s.z) as maxz '
            '  FROM cwo_system s '
            '  where s.region_id in ('
            '          select tr.region_id '
            '            from cwo_territoryregion tr, cwo_territory t '
            '            where tr.territory_id = t.id '
            '              and t.war_id = %s'
            '        )'
        )
        cursor = connection.cursor()
        cursor.execute(sql, [self.war.id])
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
            'factor': max(result[1]-result[0],result[5]-result[4]) / 1000
        }

    def ownership(self):
        sql = (
            'SELECT str.* '
            '  FROM cwo_structure str '
            '  where str.system_id in ( '
            '          select s.id '
            '            from cwo_territoryregion tr, '
            '                 cwo_territory t, '
            '                 cwo_system s '
            '            where tr.territory_id = t.id '
            '              and s.region_id = tr.region_id '
            '              and t.war_id = %(war_id)s '
            '        ) '
            '    and str.date1 < %(date)s '
            '    and %(date)s <= str.date2 '
        )
        result = {}
        for structure in Structure.objects.raw(sql, {'war_id': self.war.id, 'date': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())}):
            if not structure.system_id in result:
                result[structure.system_id] = []
            result[structure.system_id].append(structure)
        return result

    def war_system_links(self):
        sql = (
            'SELECT DISTINCT '
            '    CASE WHEN g.system_from_id > g.system_to_id THEN g.system_from_id ELSE g.system_to_id END as fid, '
            '    CASE WHEN g.system_from_id > g.system_to_id THEN g.system_to_id ELSE g.system_from_id END as tid  '
            '  FROM cwo_gate g, '
            '       cwo_system sf, '
            '       cwo_system st '
            '  where g.system_from_id = sf.id '
            '    and g.system_to_id = st.id '
            '    and sf.region_id in ( '
            '      select tr.region_id '
            '        from cwo_territoryregion tr, cwo_territory t '
            '        where tr.territory_id = t.id '
            '          and t.war_id = %s '
            '    )'
        )
        cursor = connection.cursor()
        cursor.execute(sql, [self.war.id])
        result = []
        for record in cursor.fetchall():
          result.append({'from': self.systems[record[0]], 'to': self.systems[record[1]]})
        return result
