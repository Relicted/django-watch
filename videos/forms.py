from django import forms
from .models import Video, VideoScreenshot, VideoFile
from django.utils.translation import ugettext as _


class CreateVideoItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateVideoItemForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs = {
            'class': 'btn btn-default'
        }

    original_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Original Title',
                'autocomplete': 'off'
            })
    )
    description = forms.CharField(
        label=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('Description')
            })
    )

    class Meta:
        model = Video
        fields = '__all__'


class AddScreenshots(forms.ModelForm):
    shots = forms.ImageField(
        widget=forms.FileInput(attrs={
            'multiple': True,
            'required': False
        })
    )

    class Meta:
        model = VideoScreenshot
        fields = []

    def clean(self):
        print(self.cleaned_data)
        if self.value == 'net':
            self.add_error('value', 'net =)))')
        super(AddScreenshots, self).clean()


class AddVideoFileForm(forms.ModelForm):
    files = forms.ImageField(
        widget=forms.FileInput(attrs={
            'multiple': True,
            'required': False
        })
    )
    class Meta:
        model = VideoFile
        fields = []
