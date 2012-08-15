# encoding: utf-8
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.safestring import SafeUnicode

from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView

from django.contrib import messages

from app.members.models import Member
from app.members.forms import MemberForm, UserForm, UserEditionForm


def register(request):
    member_form = MemberForm(request.POST or None)
    user_form = UserForm(request.POST or None)

    if request.method == 'POST' and user_form.is_valid() and member_form.is_valid():
        user = user_form.save()
        member = member_form.save(user)
        login = reverse('auth-login')
        messages.add_message(request, messages.INFO, SafeUnicode('Seu regitro foi realizado com sucesso. </br><a href="%s">Acesse seu perfil, para terminar de prencher se cadastro.</a>' % (login)))
        #return HttpResponseRedirect(reverse('payment', kwargs={'member_id': member.id}))
    else:
        messages.add_message(request, messages.ERROR, 'Houve um problema no seu cadastro. Verifique os campos abaixo')
    return render(request,
        'members/member_register.html',
            {
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


@login_required
def dashboard(request):
    #verifica pagamento ainda valido
    payment_valid = False
    days_left = None
    last_payment = request.user.member.payment_set.all().order_by('-date')[0]
    print datetime.now() - last_payment.valid_until
    if last_payment.valid_until is not None:
        dif = last_payment.valid_until - datetime.now()
        if dif.days > 0:
            payment_valid = True
        days_left = dif.days
    print payment_valid
    return render(request, "members/dashboard.html",
        {"payment_valid": payment_valid,
        "last_payment": last_payment,
        "days_left": days_left
         }
        )
