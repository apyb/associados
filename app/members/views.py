# -*- coding: utf-8 -*-
# Create your views here.
# encoding: utf-8
from django.shortcuts import render
from app.members.forms import MemberForm
from django.views.generic.list import ListView
from app.members.models import Member


def register(request):
    member_form = MemberForm(request.POST or None)

    if request.method == 'POST' and member_form.is_valid():
        member_form.save()
        #TODO: redirect to payment

    return render(request,
        'flatpages/form.html',
            {
            'flatpage': {'title': u'Pedido de associação à APyB'},
            'form': member_form,
            })


class MemberListView(ListView):
    model = Member
