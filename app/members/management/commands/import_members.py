# coding: utf-8
import random
import re
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.members.models import Member, Category
from app.payment.models import Payment, PaymentType, Transaction
from lista_associados import lista

class Command(BaseCommand):
    def get_username(self, email):
        email_user = email.split('@')[0]

        user_count = User.objects.filter(username__startswith=email_user).count()
        if user_count:
            username = "%s_%s" % (email_user, user_count + 1)
        else:
            username = email_user
        return username

    def get_category(self, category):
        if category == 'Estudante':
            return Category.objects.get(id=2)
        return Category.objects.get(id=1)


    def handle(self, *args, **options):
        for membro in lista:
            print("importando {0}".format(membro['nome']))
            splitted_name = re.split(" :?", membro['nome'], 1)
            user = User.objects.create(
                first_name = splitted_name[0],
                last_name = splitted_name[1],
                username=self.get_username(membro['email']),
                email=membro['email']
            )
            member = Member.objects.create(
                user=user,
                category=self.get_category(membro['tipo']),
                cpf=random.randint(0,999999999)
            )
            payment_type = PaymentType.objects.get(category=member.category)
            payment = Payment.objects.create(
                member=member,
                type=payment_type,
                date = membro['data'].date,
                valid_until = membro['data'].date + datetime.timedelta(days=payment_type.duration)
            )
            transaction = Transaction.objects.create(
                payment=payment,
                code='0',
                status='done',
                price=payment_type.price
            )