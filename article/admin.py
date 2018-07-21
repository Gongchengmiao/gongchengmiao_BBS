from django.contrib import admin
from django.db import models
from django import forms
from .models import forum_post,forum_school_info
from .models import ArticleColumn, ArticlePost, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post_title', 'pub_date', 'text')


class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'author_name', 'post_title', 'pub_date', 'text')


admin.site.register(forum_post, PostAdmin)
admin.site.register(forum_school_info, SchoolInfoAdmin)
admin.site.register(ArticleColumn)
admin.site.register(ArticlePost)
admin.site.register(Comment)