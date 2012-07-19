from django.contrib import admin
from app.members.models import Category
from models import Member, Organization, City

admin.site.register(Member)
admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(City)
