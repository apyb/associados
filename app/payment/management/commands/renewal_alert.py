# coding: utf-8
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone, translation
from app.members.models import Member
from app.payment.models import Payment

import datetime

class Command(BaseCommand):

    def _make_date_lookup_arg(self, value):
        value = datetime.datetime.combine(value, datetime.time.min)
        if settings.USE_TZ:
            value = timezone.make_aware(value, timezone.get_current_timezone())
        return value

    def handle(self, *args, **options):
        contact_email = getattr(settings, 'EMAIL_CONTACT_ADDRESS', None)

        if contact_email is None:
            raise ImproperlyConfigured('EMAIL_CONTACT_ADDRESS must be configured')

        if settings.USE_TZ:
            today = timezone.now().date()
        else:
            today = datetime.date.today()

        expiration_days = (30, 15, 7)
        expiration_dates = [today - datetime.timedelta(days=d) for d in expiration_days]
        expiration_dates += [today]

        filter_arg = None
        for d in expiration_dates:
            since = self._make_date_lookup_arg(d)
            until = self._make_date_lookup_arg(d + datetime.timedelta(days=1))

            if filter_arg is None:
                filter_arg = Q(valid_until__gte=since, valid_until__lt=until)
            else:
                filter_arg |= Q(valid_until__gte=since, valid_until__lt=until)

        if settings.USE_I18N:
            translation.activate(settings.LANGUAGE_CODE)
        for payment in Payment.objects.filter(filter_arg):
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
