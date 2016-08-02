from django.conf.urls import url
from . import views

app_name = 'cwo'

urlpatterns = [
    url(r'^$',    views.war_index,  name='war_index'),

    url(r'^new$', views.war_new,    name='war_new'),
    url(r'^create$', views.war_create,    name='war_create'),

    url(r'^(?P<war_id>[0-9]+)/edit$', views.war_edit, name='war_edit'),
    url(r'^(?P<war_id>[0-9]+)/update$', views.war_update, name='war_update'),
    url(r'^(?P<war_id>[0-9]+)/delete$', views.war_delete, name='war_delete'),

    url(r'^(?P<war_id>[0-9]+)/add_war_side$', views.add_war_side, name='add_war_side'),
    url(r'^(?P<war_id>[0-9]+)/participant/(?P<participant_id>[0-9]+)/add_alliance', views.add_alliance, name='add_alliance'),

    url(r'^(?P<war_id>[0-9]+)/add_territory$', views.add_territory, name='add_territory'),
    url(r'^(?P<war_id>[0-9]+)/territory/(?P<territory_id>[0-9]+)/add_region', views.add_region, name='add_region'),
    url(r'^(?P<war_id>[0-9]+)/territory/(?P<territory_id>[0-9]+)/region/(?P<tr_id>[0-9]+)', views.delete_region, name='delete_region'),

    url(r'^(?P<war_id>[0-9]+)/info$', views.info, name='info'),

    url(r'^alliances$', views.war_alliances,    name='war_alliances'),
    url(r'^regions$', views.war_regions,    name='war_regions'),
]
