from django import forms
from .models import ArticleColumn, ArticlePost

class ArticlePostForm(forms.ModelForm):
	class Meta:
		model = ArticlePost
		fields = ("title", "body")

