from cwo.models import Territory
from cwo.models import System
from cwo.models import Structure
from cwo.models import Region
from django.db import connection
import datetime

class WarMap:

    def __init__(self, war):
        self.war = war
        self._minmax = self.minmax()
        self.ownership = self.ownership()

        self.territories = self.territories()
        self._systems = self.systems()

        self.war_systems = self.war_systems()

    def war_systems(self):
        sql = (
            'select t.id as tid, s.id as sid '
            '  from cwo_territoryregion tr, cwo_territory t, cwo_system s '
            '  where tr.territory_id = t.id '
            '    and s.region_id = tr.region_id'
            '    and t.war_id = %s'
        )
        cursor = connection.cursor()
        cursor.execute(sql, [self.war.id])

        result = {}
        for record in cursor.fetchall():
            if record[0] not in result:
                result[record[0]] = {
                    'territory': self.territories[record[0]],
                    'systems': {},
                    'links': self.war_system_links(record[0])
                }
            result[record[0]]['systems'][record[1]] = self.system_on_territory(record[1], record[0])
        return result

    def systems(self):
        result = {}
        for s in System.objects.raw('SELECT s.* FROM cwo_system s '):
            result[s.id]=s
        return result

    def system_on_territory(self, system_id, territory_id):
        minmax = self._minmax[territory_id]
        system = self._systems[system_id]
        return {
            'name': system.name,
            'sx': (system.x - minmax['minx']) / minmax['factor'],
            'sy': (system.y - minmax['miny']) / minmax['factor'],
            'sz': 1000-(system.z - minmax['minz']) / minmax['factor']
        }

    def minmax(self):
        sql = (
            'select t.id as tid, '
            '       min(s.x) as minx, max(s.x) as maxx, '
            '       min(s.y) as miny, max(s.y) as maxy, '
            '       min(s.z) as minz, max(s.z) as maxz '
            '  from cwo_territoryregion tr, cwo_territory t, cwo_system s '
            '  where tr.territory_id = t.id '
            '    and s.region_id = tr.region_id '
            '    and t.war_id = %s '
            '  group by t.id '
        )
        cursor = connection.cursor()
        cursor.execute(sql, [self.war.id])
        result = {}
        for record in cursor.fetchall():
            if record[0] not in result:
                result[record[0]] = {}
            result[record[0]] = {
                'minx': record[1],
                'maxx': record[2],
                'miny': record[3],
                'maxy': record[4],
                'minz': record[5],
                'maxz': record[6],
                'width': record[2]-record[1],
                'height': record[4]-record[3],
                'deep': record[6]-record[5],
                'factor': max(record[2]-record[1],record[6]-record[5]) / 1000
            }

        return result

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

    def war_system_links(self, territory_id):
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
            '          and t.id = %s '
            '    )'
        )
        cursor = connection.cursor()
        cursor.execute(sql, [territory_id])
        result = []
        for record in cursor.fetchall():
          result.append({
              'from': self.system_on_territory(record[0], territory_id),
              'to': self.system_on_territory(record[1], territory_id)
          })
        return result

    def territories(self):
        result = {}
        for t in Territory.objects.raw('SELECT t.* FROM cwo_territory t where t.war_id = %s',[self.war.id]):
            result[t.id] = {
                'id': t.id,
                'name': t.name,
                'regions': Region.objects.raw('select r.* from cwo_region r where r.id in (select tr.region_id from cwo_territoryregion tr where tr.territory_id = %s)', [t.id])
            }

        return result
