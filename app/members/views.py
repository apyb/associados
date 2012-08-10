# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect

from app.members.forms import MemberForm, UserForm
from django.views.generic.list import ListView
from app.members.models import Member
from django.shortcuts import render, redirect, HttpResponse


def register(request):
    member_form = MemberForm(request.POST or None)
    user_form = UserForm(request.POST or None)
    saved = False

    if request.method == 'POST' and user_form.is_valid() and member_form.is_valid():
        user = user_form.save()
        member = member_form.save(user)
        saved = True
        return HttpResponseRedirect(reverse('payment', kwargs={'member_id':member.id}))

    return render(request,
        'members/member_register.html',
            {
            'saved': saved,
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
            self.queryset = Member.objects.filter(category__id=category)

        return super(MemberListView, self).get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        if self.query:
            context['q'] = self.query
        return context


@login_required
def member_form(request):
    member = Member.objects.get(user=request.user)
    form = MemberForm(request.POST or None, instance=member)
    if request.POST:
        if form.is_valid():
            form.save(user=request.user)

    return render(request, "members/member_form.html", {"form": form})
