# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from app.members.models import Member

class MemberListView(ListView):
    model = Member