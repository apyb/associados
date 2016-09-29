#!/usr/bin/env python
# coding: utf-8

"""
heroku login --app associados
python manage.py shell
execfile('lista_associados.py')
"""

from app.payment.models import Payment
import datetime

cyear = datetime.datetime.now().year
lyear = cyear - 1
month = datetime.datetime.now().month
day = datetime.datetime.now().day

payments = Payment.objects.filter(date__range=(datetime.date(lyear, month, day), datetime.date(cyear, month, day))).order_by('type')
estudantes = []
efetivos = []

for p in payments:
    #print p.member, p.date.strftime('%Y-%m-%d'), p.valid_until.strftime('%Y-%m-%d'), p.type.category
    if p.type.category.name == 'Efetivo':
        efetivos.append(p)
    else:
        estudantes.append(p)


print "Efetivos:"
for p in efetivos:
    print "Nome:", p.member, "Documento:", p.cpf, "Assinatura:"


print "Estudantes:"
for p in estudantes:
    print "Nome:", p.member, "Documento:", p.cpf, "Assinatura:"
