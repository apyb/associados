# encoding: utf-8
from django.db.models import Q
from django.shortcuts import render
from app.members.forms import MemberForm, UserForm
from django.views.generic.list import ListView
from app.members.models import Member


def register(request):
    member_form = MemberForm(request.POST or None)
    user_form = UserForm(request.POST or None)
    saved = False

    if request.method == 'POST' and user_form.is_valid() and member_form.is_valid():
        user = user_form.save()
        member_form.save(user)
        saved = True

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
        self.category = request.GET.get('category')

        if self.query:
            self.queryset = Member.objects.prefetch_related('user').filter(
                                                  Q(user__first_name__icontains=self.query) |
                                                  Q(user__last_name__icontains=self.query))

        if self.category:
            self.queryset = Member.objects.prefetch_related('user').filter(category=self.category)

        return super(MemberListView, self).get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        if self.query:
            context['q'] = self.query
            context['category'] = self.category
        return context
