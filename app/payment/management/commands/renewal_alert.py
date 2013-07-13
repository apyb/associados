# coding: utf-8


import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone, translation

from app.payment.models import Payment


class Command(BaseCommand):
    def _make_date_lookup_arg(self, value):
        value = timezone.datetime.combine(value, datetime.time.min)
        if settings.USE_TZ:
            value = timezone.make_aware(value, timezone.get_current_timezone())
        return value

    def handle(self, *args, **options):
        contact_email = getattr(settings, 'EMAIL_CONTACT_ADDRESS', None)

        if contact_email is None:
            raise ImproperlyConfigured('EMAIL_CONTACT_ADDRESS must be configured')

        today = timezone.now().date()

        expiration_days = (30, 15, 7)
        expiration_dates = [today - timezone.timedelta(days=d) for d in expiration_days]
        expiration_dates += [today]

        filter_arg = None
        for d in expiration_dates:
            since = self._make_date_lookup_arg(d)
            until = self._make_date_lookup_arg(d + timezone.timedelta(days=1))

            if filter_arg is None:
                filter_arg = Q(valid_until__gte=since, valid_until__lt=until)
            else:
                filter_arg |= Q(valid_until__gte=since, valid_until__lt=until)

        if settings.USE_I18N:
            translation.activate(settings.LANGUAGE_CODE)
        for payment in Payment.objects.filter(filter_arg):
            last_payment = payment.member.get_last_payment()

            if last_payment:
                last_payment_date = last_payment.valid_until.date()
                status = [last_payment_date > d for d in expiration_dates]
                already_renewed = all(status)

                # skip to send notification if already renewed
                if already_renewed:
                    continue

            valid_until_date = payment.valid_until.date()
            context = {
                'contact_email': contact_email,
                'member': payment.member,
                'url': '%s%s' % (Site.objects.get_current().domain, reverse('payment', args=[payment.member.pk])),
            }

            if valid_until_date == today:
                context['date'] = today
                subject = '[Associação Python Brasil] Anuidade vencida'
                message = render_to_string('payment/valid_until_today_email.txt',
                                           context)
            else:
                date_diff = today - valid_until_date
                context['days'] = date_diff.days
                subject = '[Associação Python Brasil] Aviso de renovação'
                message = render_to_string('payment/valid_until_email.txt',
                                           context)

            send_mail(subject, message, contact_email,
                      [payment.member.user.email], fail_silently=False)

        if settings.USE_I18N:
            translation.deactivate()
