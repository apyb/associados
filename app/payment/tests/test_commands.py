from datetime import timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from app.members.models import Member
from app.payment.management.commands.renewal_alert import (
    DAYS_BEFORE_EXPIRATION_TO_ALERT,
)
from app.payment.models import PAID, Payment, PaymentType, Transaction


class RenewalAlertTest(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.user = baker.make(User, email="naomi@pythonbrasil.org.br")
        self.member = baker.make(Member, user=self.user)
        self.type = baker.make(
            PaymentType, category=self.member.category, price=42.0, duration=365
        )
        self.payment = baker.make(
            Payment,
            member=self.member,
            type=self.type,
            valid_until=self.now,
        )
        mail.outbox = []

    def test_renewal_alert_sends_emails(self):
        test_cases = (75, 60, 45, 30, 15, 10, 7, 1, 0)
        for days in test_cases:
            mail.outbox = []
            self.payment.valid_until = self.now + timedelta(days=days)
            self.payment.save()
            expected = 1 if days in DAYS_BEFORE_EXPIRATION_TO_ALERT else 0

            call_command("renewal_alert")
            with self.subTest():
                self.assertEqual(len(mail.outbox), expected)
                if not expected:
                    continue

                self.assertEqual(mail.outbox[0].to, [self.user.email])
                self.assertIn(self.user.get_full_name(), mail.outbox[0].body)

    def test_renewal_alert_sends_email_alerts_before_membership_expires(self):
        test_cases = (30, 15, 7)
        for days in test_cases:
            mail.outbox = []
            self.payment.valid_until = self.now + timedelta(days=days)
            self.payment.save()
            call_command("renewal_alert")

            with self.subTest():
                self.assertEqual(
                    mail.outbox[0].subject,
                    "[Associação Python Brasil] Aviso de renovação",
                )

    def test_renewal_alert_sends_email_alerts_when_membership_expires(self):
        self.payment.valid_until = self.now + timedelta(days=1)
        self.payment.save()
        call_command("renewal_alert")
        self.assertEqual(
            mail.outbox[0].subject, "[Associação Python Brasil] Anuidade vencida"
        )

    def test_renewal_alert_does_not_send_email_when_already_renewed(self):
        baker.make(
            Transaction,
            payment=baker.make(
                Payment,
                member=self.member,
                type=self.type,
                valid_until=self.now + timedelta(days=2),
            ),
            status=PAID,
        )
        call_command("renewal_alert")
        self.assertFalse(mail.outbox)
