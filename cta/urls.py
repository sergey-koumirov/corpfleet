from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',                         views.index, name='index'),
    url(r'^(?P<raw_data_id>[0-9]+)/$', views.show,  name='show')
]