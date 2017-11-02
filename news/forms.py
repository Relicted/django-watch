from django import forms

from .models import Post
from videos.models import Video

class CreatePostForm(forms.ModelForm):

    video = forms.ModelMultipleChoiceField(queryset=Video.objects.all())

    class Meta:
        model = Post
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if not field == 'main_picture':
                self.fields[field].widget.attrs = {'class': 'form-control'}

    def clean(self):
        data = self.cleaned_data
        return data
