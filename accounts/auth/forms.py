from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .validators import UserRegValid
from django.contrib.auth.forms import PasswordChangeForm, UsernameField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db.models import Q

class CustomAuthenticationForm(AuthenticationForm):

    username = UsernameField(
        max_length=300,
        label='',
        widget=forms.TextInput(attrs={'autofocus': False,
                                      'class': 'form-control',
                                      'placeholder': 'Username'})
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    def clean(self):
        data = self.cleaned_data
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username))
            if not user.check_password(data.get('password')):
                self.add_error("password", _("Wrong password"))
            else:
                user_auth = authenticate(username=username, password=password)
                login(self.request, user_auth)

        except User.DoesNotExist:
            self.add_error('username',
                           _("We cant find this username in database"))


        return data


class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Email address'),
                'autocomplete': 'off'
            }
        ))

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Username'),
                'autocomplete': 'off'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm password'),
            })
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        user = UserRegValid(name=data.get('username'),
                            email=data.get('email'))

        if user.ERROR:
            for field, error in user.ERROR.items():
                self.add_error(field, error)
        return data


class ResetPasswordEmailForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Address'
        })
    )

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            self.add_error('email', _('Wrong email address'))
        return data


class ResetPasswordForm(PasswordChangeForm):
    old_password = None
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('New Password'),
                'class': 'form-control',
                'autofocus': True
            }
        ))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Confirm Password'),
                'class': 'form-control'
            }
        ))


