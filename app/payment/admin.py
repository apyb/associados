from django.contrib import admin
from app.payment.models import Payment, Transaction, PaymentType


class TransactionInline(admin.StackedInline):
    model = Transaction
    readonly_fields = ('code', 'status', 'price')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class PaymentAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]
    readonly_fields = ('member', 'type', 'date', 'valid_until')
    list_display = ('member', 'type', 'date', 'valid_until')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentType)
