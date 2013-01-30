from random import choice

from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.Form):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(label=_("Email address"), max_length=75)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
           help_text=("Enter the same password as above, for verification."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def get_username(self, email):
        email_user = email.split('@')[0]

        user_count = User.objects.filter(username__startswith=email_user).count()
        if user_count:
            username = "%s_%s" % (email_user, user_count+1)
        else:
            username = email_user
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError(_("This email address already exists. Did you forget your password?"))
        except User.DoesNotExist:
            return email

    def save(self):
        user = User()
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.get_username(user.email)

        user.is_active = True  # change to false if using email activation
        user.save()

        return user
