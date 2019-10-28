# -*- coding: utf-8 -*-
from django.conf.urls import url
from app.payment.views import NotificationView, PaymentView

urlpatterns = (
    url(r'^notification/$', NotificationView.as_view(), name='payment-notification'),
    url(r'^(?P<member_id>[\d]+)/$', PaymentView.as_view(), name='payment'),
)
