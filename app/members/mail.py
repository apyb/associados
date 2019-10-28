from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(subject, template_name, context, recipient_list,
               from_email=settings.DEFAULT_FROM_EMAIL,
               fail_silently=False):

    message_html = render_to_string(template_name, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(message_html, "text/html")

    try:
        email.send(fail_silently=fail_silently)
        return True
    except:
        return False