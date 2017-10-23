from django import forms

from .models import Post, Category



class CreatePostForm(forms.ModelForm):

    category = forms.CharField(max_length=100, required=True)
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
        category, created = Category.objects.get_or_create(
            name=data.get('category')
        )
        data['category'] = category
        return data

