#!/usr/bin/env python
# coding: utf-8

from app.payment.models import Payment
import datetime

cyear = datetime.now().year
lyear = cyear - 1
month = datetime.now().month
day = datetime.now().day

payments = Payment.objects.filter(date__range=(datetime.date(lyear, month, day), datetime.date(cyear, month, day))).order_by('type')
for p in payments:
    print p.member, p.date.strftime('%Y-%m-%d'), p.valid_until.strftime('%Y-%m-%d'), p.type.category
