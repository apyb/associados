# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView

from django.contrib import messages

from app.members.models import Member
from app.members.forms import MemberForm, UserForm, UserEditionForm


def register(request):
    member_form = MemberForm(request.POST or None)
    user_form = UserForm(request.POST or None)
    saved = False

    if request.method == 'POST' and user_form.is_valid() and member_form.is_valid():
        user = user_form.save()
        member = member_form.save(user)
        return HttpResponseRedirect(reverse('payment', kwargs={'member_id': member.id}))

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
    user_form = UserEditionForm(request.POST or None, instance=request.user)
    member_form = MemberForm(request.POST or None, instance=member)

    if request.POST:
        if member_form.is_valid() and user_form.is_valid():
            member_form.save(user=request.user)
            user_form.save()
            messages.add_message(request, messages.INFO, 'Seus dados foram atualizados com sucesso')
        else:
            messages.add_message(request, messages.INFO, 'Ocorreu um erro ao tentar salvar seus dados. verifique o form abaixo.')

    return render(request, "members/member_form.html",
        {"member_form": member_form,
        'user_form': user_form}
        )

