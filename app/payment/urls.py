from django.conf.urls import url
from app.payment.views import NotificationView, PaymentView

app_name = 'payments'

urlpatterns = (
    url(r'^notification/$', NotificationView.as_view(), name='notification'),
    url(r'^(?P<member_id>[\d]+)/$', PaymentView.as_view(), name='payment'),
)
