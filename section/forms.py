from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class FastPostForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={
        'cols': 40, 'rows': 1
    }))
    content = forms.CharField(widget=SummernoteWidget())