from django.contrib import admin
from django.db import models
from django import forms
from .models import common_member, common_member_star
from django.contrib.auth.admin import UserAdmin


# class Common_memberAdmin(admin.ModelAdmin):
#     list_display = ('username', 'status')

# succeed from UserAdmin because
# common_member succeed from AbstractUserModel


class Common_memberAdmin(UserAdmin):
    pass

# class Commmon_menber_starAdmin(admin.ModelAdmin):
#     list_display = ('uid', 'is_school_info', 'pid')



admin.site.register(common_member, Common_memberAdmin)

# admin.site.register(common_member_star, Commmon_menber_starAdmin)
