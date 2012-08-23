from random import choice

from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

NAMES = ('Graham Chapman', 'Eric Idle', 'Terry Gilliam', 'Terry Jones',
    'John Cleese', 'Michael Palin', 'Neil Innes', 'Carol Cleveland',  # monty python members/contributors
    'Arca Jeth', 'Ashka Boda', 'Vodo Baas', 'Chamma', 'Dominus', 'Exar Kun', 'Freedon Nadd',
    'Garnoo', "Gra'aton", 'Ikrit', 'Jaled Dur', 'Jassa Mroon', 'Memit Nadill', 'Odan Urr', 'Ood Bnar',
    'Ooroo', 'Master Ra\xc3\xbal', 'Shatoyo', 'Sidonra Diath', 'Ulic Qel-Droma', 'Jedon-Pan', 'Ahsoka Tano',
    'Aayla Secura', 'Adi Gallia', 'Agen Kolar', 'Anakin Skywalker', 'Annon Donnora', 'Arren Kae', 'Atris',
    'Bastila Shan', 'Barriss Offee', 'Bultar Swan', 'Cay Qel-Droma', 'Cin Drallig', 'Coleman Kcaj', 'Coleman Trebor',
    'Count Dooku', 'Daakman Barrek', 'Dark Woman', 'Malak', 'Revan', 'Darth Sion', 'Depa Billaba', 'Dorak', 'Duron Qel-Droma',
    'Dylki Maloc', 'Echuu Shen-Jon', 'Eeth Koth', 'Empatojayos Brand', 'Even Piell', 'Foul Moudama', 'Issaquah Davinta',
    'Jocasta Nu', 'Joclad Danva', 'Jedi Exile', 'Jolee Bindo', 'Juhani', 'Karn Ag', 'Kavar', 'Ki-Adi-Mundi', 'Kieran Halcyon',
    'Kit Fisto', "K'Kruhk", 'Kreia', 'Lonna Vash', 'Lumas Etima', 'Luminara Unduli', 'Luke Skywalker', 'Mace Windu',
    'Nomi Sunrider', 'Obi-Wan Kenobi', 'Oppo Rancisis', 'Pablo-Jill', 'Plo Koon', 'Qui-Gon Jinn', 'Quinlan Vos', 'Roron Corobb',
    'Roth-Del Masona', 'Saesee Tiin', 'Sha Koon', "Sha'a Gi", 'Shaak Ti', 'Serra Heto', 'Sifo-Dyas', 'Siri Tachi',
    'Sora Bulq', 'Stass Allie', 'Tan Yuster', 'Tarados Gon', 'Tarr Seirr', 'Tott Doneeta', 'Tyvokka', 'Vandar Tokare',
    'Vergere', 'Voolvif Monn', 'Yaddle', 'Yarael Poof', 'Vrook', 'Yoda', 'Zez-Kai Ell', 'Zhar', 'Alema Rar', 'Anakin Solo',
    'Callista', 'Cilghal', 'Corran Horn', "Daeshara'cor", 'Dorsk 81', 'Echuu', 'Ganner Rhysode', 'Gantoris', 'Jacen Solo',
    'Jaden Korr', 'Jaina Solo', 'Kam Solusar', 'Kirana Ti', 'Kyle Katarn', 'Kyp Durron', 'Leia Organa Solo', 'Lowbacca',
    'Mara Jade Skywalker', 'Miko Reglia', 'Nairb Oicruc', 'Osnola Reluht', 'Raynar Thul', 'Ringo Orlan',
    'Rosh Penin', 'Saba Sebatyne', 'Streen', 'Tahiri Veila', 'Tekli', 'Tenel Ka', 'Tesar Sebatyne', 'Tionne', 'Wurth Skidder',
    'Zekk', 'fyrion k-jerri', 'Max Solo', 'Igor Wohl')


class RegisterForm(forms.Form):
    """ Require email address when a user signs up """

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(label='Email address', max_length=75)
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

    def get_username(self):
        username = choice(NAMES)
        print username
        try:
            user = User.objects.filter(username__contains=username).order_by('-pk')[0]
        except IndexError:
            return username

        username = "%s %s" % (username, user.id)  # sem muita logica pra concatenar um nummero unico.
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
        user.username = self.get_username()
        user.email = self.cleaned_data["email"]
        user.is_active = True  # change to false if using email activation
        user = user.save()

        return user
