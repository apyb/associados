#!/usr/bin/env python
# coding: utf-8
#  dict(nome="", email="", tipo="Profissional", data=DateTime(""), paga=True, renovada=DateTime("")),
from django.utils.timezone import datetime


class DateTime(object):
    def __init__(self, date):
        try:
            self.date = datetime.strptime(date, "%Y-%m-%d")   
        except ValueError:
            self.date = datetime.strptime(date, "%d/%m/%Y")   


lista = [
 
]


