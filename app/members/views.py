# encoding: utf-8
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from app.members.models import Category, Member
from app.members.forms import MemberForm, UserForm
from app.authemail.forms import RegisterForm

import json


class MemberListView(ListView):
    model = Member
    paginate_by = 18

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('q')
        self.category = request.GET.get('category')

        queryset = self.get_queryset()

        if self.query:
            users = Member.objects.all()
            q = Q()
            for term in self.query.split():
                q |= Q(user__first_name__icontains=term)
                q |= Q(user__last_name__icontains=term)
                users = users.filter(q)
            queryset = users

        if self.category:
            queryset = queryset.filter(category__id=self.category)

        self.queryset = queryset.select_related("category", "user", "organization")

        return super(MemberListView, self).get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        if self.query:
            context['q'] = self.query
        if self.category:
            context['active_category'] = int(self.category)
        context['categories'] = Category.objects.all()
        return context


class SignupView(FormView):
    template_name = 'members/member_signup.html'
    form_class = RegisterForm
    success_url = reverse_lazy('members-form')

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=self.request.POST['email'],
            password=self.request.POST['password1'])
        login(self.request, user)
        messages.success(self.request, _('You\'re already registered! Complete your details to proceed\
                                         with the registration in the pool! '))
        return super(SignupView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('There was an error register'))
        return super(SignupView, self).form_invalid(form)


@login_required
def member_form(request):
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        member = Member()
    user_form = UserForm(request.POST or None, instance=request.user)
    member_form = MemberForm(request.POST or None, instance=member)
    if request.POST:
        if member_form.is_valid() and user_form.is_valid():
            member_form.save(user=request.user)
            user_form.save()
            messages.add_message(request, messages.INFO, _('Your data was updated successfully'))
            return HttpResponseRedirect(reverse('members-dashboard'))
        else:
            messages.add_message(
                request, messages.ERROR,
                _('An error occurred while trying to save your data. check the form below. '))

    return render(
        request,
        "members/member_form.html", {
            "member_form": member_form,
            'user_form': user_form
        }
    )


def member_json(request):
    data = serializers.serialize('json', Member.objects.values('user', 'category' 'mailing'))
    return JsonResponse(data)

def _retrieve_parameters(request, parameters_dict):
    received_parameters = {}

    querydict = request.GET
    for query_key in querydict:
        for param_key, param_value in parameters_dict.items():
            if param_key == query_key:
                received_parameters[param_value] = querydict[query_key]

    return received_parameters


def _search_member(params):
    result = ''
    member = Member.objects.filter(**params)

    if member:
        days_to_next_payment = member[0].get_days_to_next_payment(member[0].get_last_payment())
        if days_to_next_payment > 0:
            result = u'active'
        else:
            result = u'inactive'
    else:
        result = u'invalid'
    return {u'status': result}


def member_status(request):
    valid_parameters = {
        'cpf': 'cpf',
        'email': 'user__email',
    }
    response = ''
    params = _retrieve_parameters(request, valid_parameters)

    if params == {}:
        campos = list(valid_parameters.keys())
        campos.sort()
        error_message = 'Could not find any valid parameters. Options: %s' % campos
        response = {'error': error_message}
    else:
        response = _search_member(params)

    return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def update_category(request):
        request.user.member.change_category()
        return redirect('members-dashboard')


@login_required
def dashboard(request):
    data = {"user": request.user}
    try:
        payment_results = request.user.member.get_payment_check_list()
        data.update(payment_results)
    except Member.DoesNotExist:
        messages.add_message(request, messages.INFO, _('To access the dashboard, you need to complete your data'))
        return HttpResponseRedirect(reverse('members-form'))


    return render(
        request,
        "members/dashboard.html",
        data
    )
