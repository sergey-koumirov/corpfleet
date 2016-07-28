from django.conf.urls import url
from . import views

app_name = 'cwo'

urlpatterns = [
    url(r'^$',    views.war_index,  name='war_index'),
    url(r'^new$', views.war_new,    name='war_new'),
    url(r'^create$', views.war_new,    name='war_create')
]