from unittest import mock
from django.test import TestCase

from ..payment_service import PaymentService, PagSeguroCredentials


class PaymentServiceTest(TestCase):

    def setUp(self):
        self.payment_service = PaymentService()

    def test_payment_service_is_instantiated_with_default_config(self):
        self.assertEqual(self.payment_service.payment_system, 'PAGSEGURO')
        self.assertIsInstance(self.payment_service.credentials,
                              PagSeguroCredentials)

    def test_set_price_updates_payload(self):
        self.payment_service.set_price(34)
        self.assertIn(self.payment_service.credentials.PRICE_PAYLOAD_ATTRIBUTE,
                      self.payment_service.payload)
        self.assertEqual(
            self.payment_service.payload[
                self.payment_service.credentials.PRICE_PAYLOAD_ATTRIBUTE
            ],
            '34.00'
        )

    def test_set_description_updates_payload(self):
        description = 'Associação Python Brasil'
        self.payment_service.set_description(description)
        self.assertIn(
            self.payment_service.credentials.DESCRIPTION_PAYLOAD_ATTRIBUTE,
            self.payment_service.payload
        )
        self.assertEqual(
            self.payment_service.payload[
                self.payment_service.credentials.DESCRIPTION_PAYLOAD_ATTRIBUTE
            ],
            description
        )

    def test_set_reference_updates_payload(self):
        reference = 78798
        payment = mock.Mock()
        payment.pk = reference
        self.payment_service.set_reference(payment)
        self.assertIn(
            self.payment_service.credentials.REFERENCE_ATTRIBUTE,
            self.payment_service.payload
        )
        self.assertEqual(
            self.payment_service.payload[
                self.payment_service.credentials.REFERENCE_ATTRIBUTE
            ],
            str(reference)
        )

    def test_set_payment_system(self):
        self.assertEquals(self.payment_service.payment_system, 'PAGSEGURO')
        self.assertIsInstance(self.payment_service.credentials,
                              PagSeguroCredentials)

        self.payment_service.payment_system = 'AKAKJASD'
        with self.assertRaises(NotImplementedError):
            self.payment_service._set_payment_system()

    @mock.patch('app.payment.payment_service.PaymentService._set_headers')
    @mock.patch('app.payment.payment_service.requests.post')
    def test_payment_service_post(self, mock_post, mock_set_headers):
        ps = self.payment_service
        ps.headers = '{}'
        self.payment_service.post()
        self.assertIsNone(mock_set_headers.assert_called_once_with())

        self.assertIsNone(
            mock_post.assert_called_once_with(
                ps.credentials.checkout,
                data=ps.payload, headers=ps.headers)
        )
