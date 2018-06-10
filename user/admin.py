from django.contrib import admin
from django.db import models
from django import forms
from .models import common_member, common_member_star
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm,\
    UserCreationForm as BaseUserCreationForm
from django.conf import settings


# class Common_memberAdmin(admin.ModelAdmin):
#     list_display = ('username', 'status')

# succeed from UserAdmin because
# common_member succeed from AbstractUserModel

class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = common_member

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # if 'email_status' not in self.fields:
        #     self.fields['email_status'] =
        self.fields['email_status'].required = True


class UserChangeForm(BaseUserChangeForm):

    class Meta(BaseUserChangeForm.Meta):
        model = common_member

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email_status'].requierd = True


class Common_memberAdmin(BaseUserAdmin):
    def __init__(self, *args, **kwargs):
        super(Common_memberAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('username', 'email', 'email_status', 'is_staff', 'is_superuser')
        self.search_fields = ('username', 'email')
        self.form = UserChangeForm
        self.add_form = UserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('email_status',)}),
    )


class Commmon_menber_starAdmin(admin.ModelAdmin):
    pass



admin.site.register(common_member, Common_memberAdmin)

admin.site.register(common_member_star, Commmon_menber_starAdmin)
