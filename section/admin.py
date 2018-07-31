from django.contrib import admin
from .models import SectionForum
# from django import forms
# from .models import Forum_forum


class SectionForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'brief', 'types', 'status', 'display_order', 'posts')
    fieldsets = (
        (None, {'fields': ('name', 'brief', 'types', 'status', 'display_order', 'posts')}),
    )


admin.site.register(SectionForum, SectionForumAdmin)

