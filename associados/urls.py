from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^members/', include('app.members.urls')),
    url(r'^payment/', include('app.payment.urls')),
    url(r'^api/', include('app.api.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^logout/$', 'logout_then_login', name='auth-logout'),
    url(r'^login/', 'login', name='auth-login'),
    url(r'^password/request/$', 'password_reset'),
    url(r'^password/request/done/$', 'password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    url(r'^password/reset/done/$', 'password_reset_complete'),
    url(r'^password/change/$', 'password_change', name='auth-password-change'),
    url(r'^password/change/done/$', 'password_change_done')
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
