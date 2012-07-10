# -*- coding: utf-8 -*-
# Create your views here.
# encoding: utf-8
from django.db.models import Q
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

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('q')
        category = request.GET.get('category')
        
        if self.query:
            self.queryset = Member.objects.filter(
                                                  Q(user__first_name__icontains=self.query) |
                                                  Q(user__last_name__icontains=self.query))
        
        if category:
            self.queryset = Member.objects.filter(category=category)
        
        return super(MemberListView, self).get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        if self.query:
            context['q'] = self.query
        return context
