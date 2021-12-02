from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.test import TestCase
from app.authemail.forms import RegisterForm
from app.authemail.backends import EmailBackend


class ValidFormTest(TestCase):
    def setUp(self):
        self.data = {
            'email': 'fake_user@fake.com',
            'password1': 'fake_pass',
            'password2': 'fake_pass',
        }
        self.form = RegisterForm(data=self.data)

    def test_should_be_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_should_create_a_user(self):
        self.form.is_valid()
        user = self.form.save()
        self.assertEqual(user, User.objects.get(email=self.data['email']))

    def test_should_persist_user_data(self):
        self.form.is_valid()
        user = self.form.save()

        self.assertEqual(user.email, 'fake_user@fake.com')
        self.assertTrue(user.check_password('fake_pass'))

    def test_should_persist_the_username_of_email(self):
        self.form.is_valid()
        user = self.form.save()
        self.assertEqual(user.username, 'fake_user')

    def test_should_add_user_id_when_username_already_exists(self):
        self.form.is_valid()
        self.form.save()

        user = self.form.save()
        #expected_username = "fake_user_%s" % user.id
        # Nilo Menezes: the code is different from the test.
        expected_username = "fake_user_2"
        self.assertEqual(user.username, expected_username)


class InValidFormTest(TestCase):
    def test_should_be_invalid(self):
        data = {
            'email': '',
            'password1': '',
            'password2': '',
        }

        self.form = RegisterForm(data=data)
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.errors['email'][0], _('This field is required.'))
        self.assertEqual(self.form.errors['password1'][0], _('This field is required.'))
        self.assertEqual(self.form.errors['password2'][0], _('This field is required.'))

    def test_should_fail_if_password_mismatch(self):
        data = {
            'email': 'fake_email@fake.com',
            'password1': 'pass1',
            'password2': 'pass2',
        }

        self.form = RegisterForm(data=data)
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.errors['password2'][0], _("The two password fields didn't match."))

    def test_should_fail_if_has_another_user_with_same_email(self):
        User.objects.create(username='fake', email='fake@email.com')
        data = {
            'email': 'fake@email.com',
            'password1': 'pass',
            'password2': 'pass',
        }

        self.form = RegisterForm(data=data)
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.errors['email'][0], _("This email address already exists. Did you forget your password?"))


class EmailBackendTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username', email='test@test.com')
        self.user.set_password('test')
        self.user.save()

        self.backends = EmailBackend()

    def test_if_user_is_invalid(self):
        invalid_user = self.backends.authenticate(None, username='test_invalid_user')
        self.assertFalse(invalid_user)

    def test_if_user_is_valid(self):
        valid_user = self.backends.authenticate(None, username=self.user.username, password='test')
        self.assertTrue(valid_user)

    def test_if_user_is_valid_with_email(self):
        valid_user = self.backends.authenticate(None, username=self.user.email, password='test')
        self.assertTrue(valid_user)

    def test_invalid_password(self):
        invalid_user = self.backends.authenticate(None, username=self.user.email, password='password_error')
        self.assertFalse(invalid_user)





