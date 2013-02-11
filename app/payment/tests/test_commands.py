# coding: utf-8
from django.contrib.auth.models import User
from django.conf import settings
from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django_dynamic_fixture import G
from app.members.models import Member
from app.payment.models import Payment, Transaction, PaymentType

import datetime

class RenewalAlertConfigTest(TestCase):
    def test_renewal_alert_config_error(self):
        with self.assertRaises(ImproperlyConfigured):
            call_command('renewal_alert')

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
        expiration_dates = [now - datetime.timedelta(days=d)
            for d in expiration_days]
        expiration_dates += [now]

        payment_type = PaymentType.objects.create(
            category=self.members[0].category,
            price=50.0,
            duration=10
        )

        self.payments = [
            Payment.objects.create(member=self.members[0],
                type=payment_type,
                valid_until=expiration_dates[0]),
            Payment.objects.create(member=self.members[1],
                type=payment_type,
                valid_until=expiration_dates[1]),
            Payment.objects.create(member=self.members[2],
                type=payment_type,
                valid_until=expiration_dates[2]),
            Payment.objects.create(member=self.members[3],
                type=payment_type,
                valid_until=expiration_dates[3]),
        ]

        settings.EMAIL_CONTACT_ADDRESS = 'email@fake.com'
        call_command('renewal_alert')

    def test_renewal_alert_send_emails(self):
        self.assertEqual(len(mail.outbox), 4)

    def test_renewal_alert_send_today_email(self):
        self.assertEqual(mail.outbox[3].subject, '[Associação Python Brasil] Anuidade vencida')
        self.assertIn(self.users[3].email, mail.outbox[3].to)
        self.assertTrue(mail.outbox[3].body.find(self.users[3].get_full_name()) != -1)

    def test_renewal_alert_send_other_days_email(self):
        for index, email in enumerate(mail.outbox[:3]):
            self.assertEqual(email.subject, '[Associação Python Brasil] Aviso de renovação')
            self.assertIn(self.users[index].email, email.to)
            self.assertTrue(email.body.find(self.users[index].get_full_name()) != -1)
