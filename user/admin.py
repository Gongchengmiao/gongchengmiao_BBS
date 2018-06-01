from django.contrib import admin
from django.db import models
from django import forms
from .models import common_member,common_member_star


class Common_memberAdmin(admin.ModelAdmin):
    list_display = ('uid','username','status')


class Commmon_menber_starAdmin(admin.ModelAdmin):
    list_display = ('uid','is_school_info','pid')



admin.site.register(common_member, Common_memberAdmin)
admin.site.register(common_member_star, Commmon_menber_starAdmin)
