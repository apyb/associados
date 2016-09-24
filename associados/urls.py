from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = [
    url(r'^members/', include('app.members.urls')),
    url(r'^payment/', include('app.payment.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^municipios_app/', include('municipios.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
