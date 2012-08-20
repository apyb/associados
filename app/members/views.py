# encoding: utf-8
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import SafeUnicode
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from app.members.models import Member
from app.members.forms import MemberForm, UserForm
from authemail.forms import RegisterForm


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


class SignupView(FormView):
    template_name = 'members/member_signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('members-form')

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=self.request.POST['username'],
            password=self.request.POST['password1']
        )
        login(self.request, user)
        messages.success(self.request, 'Você está cadastrado! Complete os seus dados para\
         prosseguir com o registro na associação!')
        return super(SignupView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao cadastrar-se')
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
            messages.add_message(request, messages.INFO, 'Seus dados foram atualizados com sucesso')
            return HttpResponseRedirect(reverse('members-dashboard'))
        else:
            messages.add_message(request, messages.ERROR, 'Ocorreu um erro ao tentar salvar seus dados. verifique o form abaixo.')

    return render(request,
        "members/member_form.html",{
            "member_form": member_form,
            'user_form': user_form
        }
    )


@login_required
def dashboard(request):
    try:
        payment_results = request.user.member.get_payment_check_list()
    except Member.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Para acessar os dashboard, você precisa completar os seus dados')
        return HttpResponseRedirect(reverse('members-form'))

    return render(request,
        "members/dashboard.html",{
            "expired": payment_results['expired'],
            "last_payment": payment_results['last_date'],
            "days_left": payment_results['days_left']
        }
    )


def register_old(request):
    member_form = MemberForm(request.POST or None)
    user_form = UserForm(request.POST or None)

    if request.method == 'POST':
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save()
            member = member_form.save(user)
            login = reverse('auth-login')
            messages.add_message(request, messages.INFO, SafeUnicode('Seu regitro foi realizado com sucesso. </br><a href="%s">Acesse seu perfil, para terminar de prencher se cadastro.</a>' % (login)))
        else:
            messages.add_message(request, messages.ERROR, 'Houve um problema no seu cadastro. Verifique os campos abaixo')
    return render(request,
        'members/member_register.html',{
            'user_form': user_form,
            'member_form': member_form
        }
    )


def register(request):
    user_form = RegisterForm()
    if request.method == 'POST':
        #data = request.POST.copy()  # so we can manipulate data
        user_form = RegisterForm(request.POST or None)

        if user_form.is_valid():

            user_form.save()
            login = reverse('auth-login')
            messages.add_message(request, messages.INFO, SafeUnicode('Seu regitro foi realizado com sucesso. </br><a href="%s">Acesse seu perfil, para terminar de prencher se cadastro.</a>' % (login)))
            return HttpResponseRedirect(reverse('auth-login'))
        else:
            messages.add_message(request, messages.ERROR, 'Houve um problema no seu cadastro. Verifique os campos abaixo')
    return render(request, 'members/member_register.html', {'user_form': user_form})
