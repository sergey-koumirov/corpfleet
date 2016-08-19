from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^cta/', include('cta.urls') ),
    url(r'^admin/', admin.site.urls),
    url(r'^wars/', include('cwo.urls')),
    url(r'^$', views.index, name='index' ),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'},  name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',  name='logout'),
]
