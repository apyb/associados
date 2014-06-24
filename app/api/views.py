from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404

from app.members.models import Member

import json


def verify_membership(request):
    email = request.GET.get('email', '')
    token = request.GET.get('token', '')
    if token == settings.PYBR10_AUTH_TOKEN:
        m = get_object_or_404(Member, user__email=email)
        status = m.get_payment_check_list()
        response = {
            'expired': status['expired'],
            'days_left': status['days_left']
        }

        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse(status=401)
