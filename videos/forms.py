from django import forms
from .models import Video, VideoScreenshot, VideoFile, WatchingList
from django.utils.translation import ugettext as _


class CreateVideoItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateVideoItemForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs = {
            'class': 'select select--white'
        }
        self.fields['series_status'].widget.attrs = {
            'class': 'select select--white',
            'required': False
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


class AddVideoToList(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddVideoToList, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'select select--white'
            })

    class Meta:
        model = WatchingList
        exclude = ['user', 'video']