# corpfleet

python3 manage.py runserver

python3 manage.py makemigrations cwo
python3 manage.py migrate

python3 manage.py makemigrations --empty cwo

pip3 install mysqlclient
pip3 install sqlparse
pip3 install preston

python manage.py createsuperuser --username=joe --email=joe@example.com


select d, sum(x.adm)
  from(
	SELECT s1.id, s1.alliance_id, s1.defence as adm, GREATEST(s1.date1, pa1.date1) as d
	  FROM cwo_dev.cwo_structure s1,
           cwo_participantalliance pa1
      where pa1.alliance_id = s1.alliance_id
        and pa1.participant_id = 17
        and pa1.date1 <= s1.date2
        and pa1.date2 >= s1.date1
        and s1.system_id in (select id
                               from cwo_system
                               where region_id in (select region_id from cwo_territoryregion where territory_id = 4)
							)
	union
	SELECT s2.id, s2.alliance_id, -1*s2.defence as adm, LEAST(s2.date2, pa2.date2) as d
	  FROM cwo_dev.cwo_structure s2,
           cwo_participantalliance pa2
      where pa2.alliance_id = s2.alliance_id
        and pa2.participant_id = 17
        and pa2.date1 <= s2.date2
        and pa2.date2 >= s2.date1
        and s2.system_id in (select id
                               from cwo_system
                               where region_id in (select region_id from cwo_territoryregion where territory_id = 4)
							)
  ) x
  group by d
  order by d