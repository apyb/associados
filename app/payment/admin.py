# coding: utf-8


from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app.payment.models import Payment, Transaction, PaymentType


class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 0


def make_paid(modeladmin, request, queryset):
    for payment in queryset:
        if payment.last_transaction and payment.last_transaction.status != 3:
            payment.last_transaction.status = 3
            payment.last_transaction.save()


make_paid.short_description = _("Set last transactions as paid")


def last_transaction_name(obj):
    return obj.last_transaction.get_status_display()


last_transaction_name.short_description = _('Last Transaction')


class PaymentAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]
    search_fields = ('member__user__first_name', 'member__user__last_name', 'member__user__email')
    list_display = ('member', 'type', 'date', 'valid_until', last_transaction_name)
    actions = [make_paid]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentType)
