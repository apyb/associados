# Create your views here.
# encoding: utf-8
from django.shortcuts import render
from app.auth.forms import MemberForm


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
