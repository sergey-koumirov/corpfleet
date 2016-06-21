from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^cta/', include('cta.urls') ),
    url(r'^admin/', admin.site.urls),
]
