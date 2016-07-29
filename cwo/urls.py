from django.conf.urls import url
from . import views

app_name = 'cwo'

urlpatterns = [
    url(r'^$',    views.war_index,  name='war_index'),
    url(r'^new$', views.war_new,    name='war_new'),
    url(r'^(?P<war_id>[0-9]+)/edit$', views.war_edit, name='war_edit'),
    url(r'^create$', views.war_create,    name='war_create'),
    url(r'^alliances$', views.war_alliances,    name='war_alliances'),
]
