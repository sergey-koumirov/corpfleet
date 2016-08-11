from cwo.models import Territory
from cwo.models import System
from cwo.models import Structure
from cwo.models import Region
from django.db import connection
import datetime
from django.utils import timezone

class WarMap:

    def __init__(self, war):
        self.war = war

    def as_json(self):
        self._minmax = self.minmax()
        self._systems = self.systems()
        return {
            'territories': self.territory_infos_as_json(),
            'structures': self.ownership(),
            'participants': self.participants(),
        }

    def territory_infos_as_json(self):
        result = {}
        for t in Territory.objects.filter(war_id=self.war.id):
            result[t.id] = {
                'id': t.id,
                'name': t.name,
                'regions': [ {'id': r.id, 'name': r.region.name} for r in t.territoryregion_set.all()],
                'powers': self.powers_as_json(t.id),
                'systems': self.war_systems_as_json(t.id),
                'links': self.war_system_links(t.id)
            }

        return result

    def territories_as_json(self):
        result = {}
        for t in Territory.objects.filter(war_id=self.war.id):
            result[t.id] = {
                'id': t.id,
                'name': t.name,
                'regions': [ {'id': r.id, 'name': r.region.name} for r in t.territoryregion_set.all()],
            }
        return result

    def war_systems_as_json(self, tid):
        sql = (
            'select s.id as sid '
            '  from cwo_territoryregion tr, cwo_system s '
            '  where s.region_id = tr.region_id'
            '    and tr.territory_id = %s'
        )
        cursor = connection.cursor()
        cursor.execute(sql, [tid])

        result = []
        for record in cursor.fetchall():
            result.append(self.system_on_territory(record[0], tid))
        return result

    # ------------------------------------------------------------------------------------------------------------------


    def load(self):
        self._minmax = self.minmax()
        self.ownership = self.ownership()

        self.territories = self.territories()
        self._systems = self.systems()

        self.war_systems = self.war_systems()
        self.participants = self.participants()

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

    def systems_json(self):
        result = {
            "nodes": [],
            "edges":[],
        }
        nodes = result["nodes"]
        for s in System.objects.raw('SELECT s.* FROM cwo_system s where s.id < 31000000 '):
            nodes.append({'id': s.id, 'label': s.name, 'x': s.x/1000000000000000, 'y':s.z/1000000000000000, 'color': '#ff0000'})
        return result

    def system_on_territory(self, system_id, territory_id):
        minmax = self._minmax[territory_id]
        system = self._systems[system_id]
        return {
            'id': system.id,
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
            f = self.system_on_territory(record[0], territory_id)
            t = self.system_on_territory(record[1], territory_id)
            result.append({
                'f': {'sx': f['sx'], 'sz': f['sz']},
                't': {'sx': t['sx'], 'sz': t['sz']}
            })
        return result

    def territories(self):
        result = {}
        for t in Territory.objects.raw('SELECT t.* FROM cwo_territory t where t.war_id = %s',[self.war.id]):
            result[t.id] = {
                'id': t.id,
                'name': t.name,
                'regions': Region.objects.raw('select r.* from cwo_region r where r.id in (select tr.region_id from cwo_territoryregion tr where tr.territory_id = %s)', [t.id]),
                'powers': self.powers(t.id)
            }
        return result

    def powers_as_json(self, tid):
        sql = (
            'select d, sum(x.adm) as power'
            '  from( SELECT s1.id, s1.alliance_id, s1.defence as adm, GREATEST(s1.date1, pa1.date1) as d '
            '          FROM cwo_dev.cwo_structure s1, '
            '               cwo_participantalliance pa1 '
            '               where pa1.alliance_id = s1.alliance_id '
            '                 and pa1.participant_id = %(pid)s '
            '                 and pa1.date1 <= s1.date2 '
            '                 and pa1.date2 >= s1.date1 '
            '                 and s1.system_id in (select id '
            '                                        from cwo_system '
            '                                        where region_id in (select region_id from cwo_territoryregion where territory_id = %(tid)s) '
            '                                      ) '
            '        union '
            '        SELECT s2.id, s2.alliance_id, -1*s2.defence as adm, LEAST(s2.date2, pa2.date2) as d '
            '          FROM cwo_dev.cwo_structure s2, '
            '               cwo_participantalliance pa2 '
            '          where pa2.alliance_id = s2.alliance_id '
            '            and pa2.participant_id = %(pid)s '
            '            and pa2.date1 <= s2.date2 '
            '            and pa2.date2 >= s2.date1 '
            '            and s2.system_id in (select id '
            '                                   from cwo_system '
            '                                   where region_id in (select region_id from cwo_territoryregion where territory_id = %(tid)s) '
            '                                ) '
            '  ) x '
            '  where d < \'9999-12-13\''
            '  group by d '
            '  order by d '
        )

        result = []
        for p in self.war.participant_set.all():
            cursor = connection.cursor()
            cursor.execute(sql, {'tid': tid, 'pid': p.id})
            power = 0
            data=[]
            for record in cursor.fetchall():
                power = power + record[1]
                data.append([record[0].timestamp()*1000, power])
            if len(data)>0:
                data.append([timezone.now().timestamp()*1000,power])

                result.append({
                    'name': p.name,
                    'color': p.color,
                    'data': data,
                })

        return result


    def ownership(self):
        sql = (
            'SELECT concat(\'s\',s.system_id, case s.type_id when 32458 then \'h\' when 32226 then \'t\' else \'s\' end) as sid, '
            '       s.alliance_id,'
            '       s.defence, '
            '       s.date1, '
            '       s.date2 '
            '  FROM cwo_system sys, '
            '       cwo_structure s '
            '  where s.system_id = sys.id '
            '    and sys.region_id in ( '
            '          select tr.region_id '
            '            from cwo_territoryregion tr, '
            '                 cwo_territory t '
            '            where tr.territory_id = t.id '
            '              and t.war_id = %(war_id)s '
            '        ) '
            '    and s.date1 < %(date2)s '
            '    and s.date2 > %(date1)s '
            '  order by sid, date1'
        )
        cursor = connection.cursor()
        cursor.execute(sql, {'war_id': self.war.id, 'date1':self.war.date1, 'date2':self.war.date2})

        result = {}
        for record in cursor.fetchall():
            if record[0] not in result:
                result[record[0]] = []
            result[record[0]].append({
                'aid': record[1],
                'm': record[2],
                'd1': '{0:%Y-%m-%d %H:%M:%S}'.format(record[3]),
                'd2': '{0:%Y-%m-%d %H:%M:%S}'.format(record[4]),
            })

        return result

    def participants(self):
        sql = (
            'SELECT pa.alliance_id, p.id, p.name, pa.date1, pa.date2, p.color '
            '    FROM cwo_participantalliance pa, '
            '         cwo_participant p '
            '    where p.id = pa.participant_id '
            '      and p.war_id=%s '
            '    order by pa.alliance_id, pa.date1 '
        )
        cursor = connection.cursor()
        cursor.execute(sql, [self.war.id])
        result = {}
        for record in cursor.fetchall():
            if record[0] not in result:
                result[record[0]] = []
            result[record[0]].append({
                'pid': record[1],
                'name': record[2],
                'd1': '{0:%Y-%m-%d %H:%M:%S}'.format(record[3]),
                'd2': '{0:%Y-%m-%d %H:%M:%S}'.format(record[4]),
                'color': record[5],
            })
        return result
