from django.contrib import admin
from django.db import models
from django import forms
from .models import ArticleColumn, ArticlePost


class PostAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post_title', 'pub_date', 'text')


class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'author_name', 'post_title', 'pub_date', 'text')


admin.site.register(ArticleColumn)
admin.site.register(ArticlePost)