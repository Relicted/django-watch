from django import forms
from .models import UserMessage

from django.template.defaultfilters import striptags


class ReportSuggestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'placeholder': self.fields[field].label
            }

    class Meta:
        model = UserMessage
        fields = ('type', 'theme', 'text')
        widgets = {
            'text': forms.Textarea()
        }


    def clean(self):
        data = super(ReportSuggestionForm, self).clean()
        return data