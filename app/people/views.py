# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from app.people.models import UserProfile

class MemberListView(ListView):
    model = UserProfile