from django import forms

from tutorial.models import BaseModel
from .models import Profile
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import PasswordChangeForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'picture', 'email_confirmed')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


class PictureForm(forms.Form):
    picture = forms.ImageField(
        label=_('Upload Picture'),
        widget=forms.FileInput(
            attrs={'class': 'hidden'}))


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'placeholder': self.fields[field].label,
                'class': 'form-control'
            }

