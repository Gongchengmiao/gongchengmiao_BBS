from django.contrib import admin
from django.db import models
from django import forms
from .models import ArticleColumn, ArticlePost, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pid', 'title','is_school_info', 'author')
    fieldsets = (
        (None, {'fields': ('title', 'is_school_info', 'author', 'ueditor_body', 'isElite','users_like',
                           'section_belong_fk', 'slug')}),
    )


admin.site.register(ArticleColumn)
admin.site.register(ArticlePost, ArticleAdmin)
admin.site.register(Comment)
