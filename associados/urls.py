from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app.payment import urls as payment_urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^members/', include('app.members.urls')),
    url(r'^payment/', include(payment_urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
