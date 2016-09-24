# coding: utf-8


from django.contrib import admin
from app.members.models import Category, Member, Organization, City
#from models import Member, Organization, City


class MemberAdmin(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    list_display = ('full_name', 'category')


admin.site.register(Member, MemberAdmin)
admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(City)
