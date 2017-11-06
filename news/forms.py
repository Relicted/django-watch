from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext as _
from .models import Post
from videos.models import Video

class CreatePostForm(forms.ModelForm):
    #
    # videos = forms.CharField(
    #     label='Related Videos',
    #     help_text='CREATE AJAX SEARCH AND CHECKBOX FOR VIDEO'
    # )

    video = forms.ModelMultipleChoiceField(
        queryset=Video.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if not self.fields[field].widget.__class__.__name__ == 'FileInput':
                self.fields[field].widget.attrs = {
                    'placeholder': self.fields[field].label
                }
                self.fields[field].label = ''

    class Meta:
        model = Post
        exclude = ('user',)
        widgets = {
            'description': forms.Textarea(),
            'text': forms.Textarea(),
            'main_picture': forms.FileInput(attrs={'class': 'hidden'})
        }

    def clean(self):
        data = self.cleaned_data
        return data
