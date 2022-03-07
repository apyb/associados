from contextlib import contextmanager
from datetime import timedelta

import pytz
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Max, Q, Subquery
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone, translation

from app.payment.models import Payment

TIME_ZONE = pytz.timezone(settings.TIME_ZONE)
DAYS_BEFORE_EXPIRATION_TO_ALERT = (60, 30, 15, 7, 1)


@contextmanager
def translate():
    if settings.USE_I18N:
        translation.activate(settings.LANGUAGE_CODE)

    yield

    if settings.USE_I18N:
        translation.deactivate()


def send_apyb_mail(**kwargs):
    for key, default in settings.SEND_EMAIL_DEFAULTS.items():
        kwargs[key] = kwargs.get(key, default)

    if not kwargs["subject"].startswith(settings.EMAIL_SUBJECT_PREFIX):
        kwargs["subject"] = f"[Associação Python Brasil] {kwargs['subject']}"

    if "message" not in kwargs:
        template = kwargs.pop("template")
        context = kwargs.pop("context")
        kwargs["message"] = render_to_string(template, context)

    return send_mail(**kwargs)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.contact_email = settings.EMAIL_CONTACT_ADDRESS
        if not self.contact_email:
            raise ImproperlyConfigured("EMAIL_CONTACT_ADDRESS not configured")

        self.now = timezone.now()
        self.today = TIME_ZONE.normalize(self.now).date()
        self.tomorrow = TIME_ZONE.normalize(self.now + timedelta(days=1)).date()
        self.alert_dates = tuple(self._alert_dates())

    def _alert_dates(self):
        for days in DAYS_BEFORE_EXPIRATION_TO_ALERT:
            when = self.now + timedelta(days)
            yield TIME_ZONE.normalize(when).date()

    @property
    def payments(self):
        # This subquery gets member whose subscription expires in MORE than 60
        # days (or the maximum listed in DAYS_BEFORE_EXPIRATION_TO_ALERT); i.e.
        # members who we are NOT emailing (even if they happen to have another
        # payment expiring in the next 60 days).
        active_members = Subquery(
            Payment.objects.annotate(expires_on=Max("valid_until"))
            .filter(expires_on__date__gt=max(self.alert_dates))
            .values("member_id")
        )
        return (
            Payment.objects.exclude(member__in=active_members)
            .filter(valid_until__date__in=self.alert_dates)
            .select_related("member")
        )

    def context_for(self, payment):
        domain = Site.objects.get_current().domain
        path = reverse("payments:payment", args=[payment.member.pk])
        return {
            "contact_email": self.contact_email,
            "member": payment.member,
            "url": f"{domain}{path}",
            "date": self.today,
            "days": (payment.valid_until.date() - self.today).days,
        }

    def handle(self, *_args, **options):
        with translate():
            for payment in self.payments:
                valid_until = TIME_ZONE.normalize(payment.valid_until).date()
                if valid_until == self.tomorrow:
                    subject = "Anuidade vencida"
                    template = "payment/valid_until_today_email.txt"
                else:
                    subject = "Aviso de renovação"
                    template = "payment/valid_until_email.txt"

                user = payment.member.user.get_full_name()
                self.stdout.write(f"Emailing {user}: {subject}")
                send_apyb_mail(
                    subject=subject,
                    template=template,
                    context=self.context_for(payment),
                    recipient_list=[payment.member.user.email],
                )
