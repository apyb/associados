from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app.payment import urls as payment_urls

admin.autodiscover()

urlpatterns = [
    url(r'^members/', include('app.members.urls', namespace='members')),
    url(r'^payment/', include(payment_urls)),
    url(r'^admin/doc/', include(('django.contrib.admindocs.urls', 'doc'), namespace='doc')),
    url(r'^admin/', admin.site.urls),
    url(r'^municipios_app/', include('municipios.urls')),
    url(r'^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
