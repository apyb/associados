#!/usr/bin/env python

"""
heroku login
heroku run --app associados bash
python manage.py shell
execfile('lista_associados.py')
"""

from django.contrib.auth.models import User
from app.payment.models import Payment
import datetime

cyear = datetime.datetime.now().year
lyear = cyear - 1
month = datetime.datetime.now().month
day = datetime.datetime.now().day

payments = Payment.objects.filter(date__range=(datetime.date(lyear, month, day), datetime.date(cyear, month, day))).order_by('type').order_by('member__user__first_name') # valeu @cadu-leite
user_list = User.objects.all()
user_email = dict(user_list.values_list("username", "email"))
estudantes = []
efetivos = []

for p in payments:
    #print p.member, p.date.strftime('%Y-%m-%d'), p.valid_until.strftime('%Y-%m-%d'), p.type.category
    if p.type.category.name == 'Efetivo':
        efetivos.append(p)
    else:
        estudantes.append(p)


# TODO: inserir user_email[p.member.user]
print "Efetivos:"
for p in efetivos:
    print "Nome:", p.member, "CPF:", p.member.cpf, "Email:", p.member.user.email, "Ass:"


print "Estudantes:"
for p in estudantes:
    print "Nome:", p.member, "CPF:", p.member.cpf, "Email:", p.member.user.email, "Ass:"
