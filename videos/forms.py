from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Video, VideoScreenshot, VideoFile, WatchingList, Genre
from django.utils.translation import ugettext as _


class CreateVideoItemForm(forms.ModelForm):

    original_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Original Title',
                'autocomplete': 'off'
            })
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=FilteredSelectMultiple('genres', is_stacked=False))

    description = forms.CharField(
        label=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('Description')
            })
    )

    shots = forms.ImageField(
        widget=forms.FileInput(attrs={
            'multiple': True,
            'required': False
        })
    )

    class Meta:
        model = Video
        fields = ('content',
                  'series_status',
                  'original_title',
                  'genres',
                  'poster',
                  'description',
                  'shots')

    def clean(self):
        data = super(CreateVideoItemForm, self).clean()
        series = ['series', 'animationseries']
        if data.get('content') in series and not data.get('series_status'):
            self.add_error(
                'series_status', _('This field is required for series items.'))
        return data


class AddScreenshots(forms.ModelForm):


    class Meta:
        model = VideoScreenshot
        fields = []


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
                'class': 'form-control'
            })
        self.instance = kwargs.get('instance')

    class Meta:
        model = WatchingList
        exclude = ['user', 'video']

    def clean(self):
        data = super(AddVideoToList, self).clean()
        if data['is_favorite']:
            self.is_favorite = True
        return data