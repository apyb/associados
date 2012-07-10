# -*- coding: utf-8 -*-
# Create your views here.
# encoding: utf-8
from django.shortcuts import render
from app.members.forms import MemberForm, UserForm
from django.views.generic.list import ListView
from app.members.models import Member





def register(request):
    member_form = MemberForm(request.POST or None)
    user_form = UserForm(request.POST or None)
    if request.method == 'POST' and user_form.is_valid() and member_form.is_valid():
        user = user_form.save()
        member_form.save(user)

    return render(request,
        'flatpages/form.html',
            {
            'flatpage': {'title': u'Pedido de associação à APyB'},
            'user_form': user_form,
            'member_form': member_form,
            })


class MemberListView(ListView):
    model = Member
