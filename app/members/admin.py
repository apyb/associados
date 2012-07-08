from django.contrib import admin
from models import Member, Organization, City
from django.contrib.auth.models import User


admin.site.register(Member)
admin.site.register(Organization)
admin.site.register(City)
