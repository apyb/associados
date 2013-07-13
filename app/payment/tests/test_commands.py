# -*- coding: utf-8 -*-


import datetime

from django.contrib.auth.models import User
from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from django_dynamic_fixture import G

from app.members.models import Member
from app.payment.models import Payment, PaymentType, Transaction


class RenewalAlertTest(TestCase):
    def setUp(self):
        self.users = [
            G(User),
            G(User),
            G(User),
            G(User),
        ]

        self.members = [
            G(Member, user=self.users[0]),
            G(Member, user=self.users[1]),
            G(Member, user=self.users[2]),
            G(Member, user=self.users[3]),
        ]

        now = timezone.now()
        expiration_days = (30, 15, 7)
        self.expiration_dates = [now - datetime.timedelta(days=d)
                            for d in expiration_days]
        self.expiration_dates += [now]

        self.payment_type = PaymentType.objects.create(
            category=self.members[0].category,
            price=50.0,
            duration=10
        )

        self.payments = [
            Payment.objects.create(member=self.members[0],
                                   type=self.payment_type,
                                   valid_until=self.expiration_dates[0]),
            Payment.objects.create(member=self.members[1],
                                   type=self.payment_type,
                                   valid_until=self.expiration_dates[1]),
            Payment.objects.create(member=self.members[2],
                                   type=self.payment_type,
                                   valid_until=self.expiration_dates[2]),
            Payment.objects.create(member=self.members[3],
                                   type=self.payment_type,
                                   valid_until=self.expiration_dates[3]),
        ]

        settings.EMAIL_CONTACT_ADDRESS = 'email@fake.com'

    def test_renewal_alert_send_emails(self):
        call_command('renewal_alert')

        self.assertEqual(len(mail.outbox), 4)

    def test_renewal_alert_send_today_email(self):
        call_command('renewal_alert')

        self.assertEqual(mail.outbox[3].subject, '[Associação Python Brasil] Anuidade vencida')
        self.assertIn(self.users[3].email, mail.outbox[3].to)
        self.assertTrue(mail.outbox[3].body.find(self.users[3].get_full_name()) != -1)

    def test_renewal_alert_send_other_days_email(self):
        call_command('renewal_alert')

        for index, email in enumerate(mail.outbox[:3]):
            self.assertEqual(email.subject, '[Associação Python Brasil] Aviso de renovação')
            self.assertIn(self.users[index].email, email.to)
            self.assertTrue(email.body.find(self.users[index].get_full_name()) != -1)

    def test_renewal_alert_not_send_email_when_already_renewed(self):
        self.users += [
            G(User),
        ]

        self.members += [
            G(Member, user=self.users[4]),
        ]

        post_expiration_date = timezone.now() + datetime.timedelta(days=1)
        delta = datetime.timedelta(days=self.payment_type.duration)
        dates = [d - delta for d in self.expiration_dates + [post_expiration_date]]

        self.payments += [
            Payment.objects.create(member=self.members[4],
                                   type=self.payment_type,
                                   date=dates[0],
                                   valid_until=self.expiration_dates[0]),
            Payment.objects.create(member=self.members[4],
                                   type=self.payment_type,
                                   date=dates[1],
                                   valid_until=self.expiration_dates[1]),
            Payment.objects.create(member=self.members[4],
                                   type=self.payment_type,
                                   date=dates[2],
                                   valid_until=self.expiration_dates[2]),
            Payment.objects.create(member=self.members[4],
                                   type=self.payment_type,
                                   date=dates[3],
                                   valid_until=self.expiration_dates[3]),
            Payment.objects.create(member=self.members[4],
                                   type=self.payment_type,
                                   date=dates[4],
                                   valid_until=post_expiration_date),
        ]

        G(Transaction, payment=self.payments[-5], status='3')
        G(Transaction, payment=self.payments[-4], status='3')
        G(Transaction, payment=self.payments[-3], status='3')
        G(Transaction, payment=self.payments[-2], status='3')
        G(Transaction, payment=self.payments[-1], status='3')

        call_command('renewal_alert')

        for email in mail.outbox:
            self.assertNotIn(self.users[4].email, email.to)
            self.assertFalse(email.body.find(self.users[4].get_full_name()) != -1)
