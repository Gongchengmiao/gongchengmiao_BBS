from django import forms
from .models import ArticleColumn, ArticlePost
from .models import Comment

class ArticlePostForm(forms.ModelForm):
	class Meta:
		model = ArticlePost
		fields = ("title", "body")


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ("body",)