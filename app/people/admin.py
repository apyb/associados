from django.contrib import admin
from models import UserProfile, Organization, City
from django.contrib.auth.models import User


admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(City)
