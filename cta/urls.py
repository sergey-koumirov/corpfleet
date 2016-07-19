from django.conf.urls import url
from . import views

app_name = 'cta'

urlpatterns = [
    url(r'^$',                         views.index, name='index'),
    url(r'^(?P<raw_data_id>[0-9]+)/$', views.show,  name='show'),
    url(r'^(?P<raw_data_id>[0-9]+)/update$', views.update,  name='update')
]