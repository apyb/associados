from django.conf.urls import url
from app.members.views import MemberListView, member_form, dashboard, update_category, SignupView, member_status, member_json

app_name = 'members'

urlpatterns = (
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^list/$', MemberListView.as_view(), name='list'),
    url(r'^update/$', member_form, name='form'),
    url(r'^update-category/$', update_category, name='update-category'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^status/$', member_status, name='status'),
    url(r'^json-list/$', member_json, name='json'),
)
