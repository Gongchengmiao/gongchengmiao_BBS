from django import forms
from DjangoUeditor.forms import UEditorField
from .models import ArticleColumn, ArticlePost
from .models import Comment


# class ArticlePostForm(forms.ModelForm):
# 	class Meta:
# 		model = ArticlePost
# 		fields = ("title", "ueditor_body")

class ArticlePostForm(forms.Form):
    title = forms.CharField()
    content = UEditorField('内容', width=800, height=900, toolbars="full",
                           imagePath="images/", filePath="files/",upload_settings = {"imageMaxSize": 1204000},settings = {})


class CommentForm(forms.Form):
    comment_body = UEditorField('内容', width=400, height=300, toolbars="mini",
                           imagePath="images/", filePath="files/",upload_settings = {"imageMaxSize": 1204000},settings = {})

