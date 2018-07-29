from django.contrib import admin
from django.db import models
from django import forms
from .models import common_member, common_member_star, follower_pair, common_member_action_log ,section_follow_pair
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm,\
    UserCreationForm as BaseUserCreationForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.conf import settings


# class Common_memberAdmin(admin.ModelAdmin):
#     list_display = ('username', 'status')

# succeed from UserAdmin because
# common_member succeed from AbstractUserModel

class UserCreationForm(BaseUserCreationForm):

    # email_status = forms.CharField(
    #     label=_("Email_status"),
    #     strip=False,
    #     widget=forms.CheckboxInput,
    #     # help_text=password_validation.password_validators_help_text_html(),
    # )

    class Meta(BaseUserCreationForm.Meta):
        model = common_member
        # fields = ("username", "email_status")
        # field_classes = BaseUserCreationForm.Meta.field_classes.update({"email_status": forms.EmailField})
        # fields['email_status'].requierd = True

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['email_status'].required = True

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email_status = self.cleaned_data["email_status"]
    #     if commit:
    #         user.save()
    #     return user



class UserChangeForm(BaseUserChangeForm):

    class Meta(BaseUserChangeForm.Meta):
        model = common_member

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.list_display = ('username', 'gender', 'profile', 'posts', 'follow_list', 'email', 'email_status', 'is_staff', 'is_superuser')
        #self.fields['email_status'].requierd = True


class Common_memberAdmin(BaseUserAdmin):
    def __init__(self, *args, **kwargs):
        super(Common_memberAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('username','gender', 'email', 'email_status','follow_list', 'is_staff', 'is_superuser')
        self.search_fields = ('username', 'email')
        self.form = UserChangeForm
        self.add_form = UserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (
        ('personal info', {'fields': ('email_status','gender','posts','profile', 'following', 'followed','portrait')}),
    )


class Commmon_menber_starAdmin(admin.ModelAdmin):
    list_display = ('uid', 'pid')

class followers_Adim(admin.ModelAdmin):
    list_display=('followed','by')

class User_action_log_Admin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'action','dateline')
    fieldsets = (
        (None, {'fields': ('id', 'uid', 'action','is_school_info', 'pid')}),
    )

admin.site.register(common_member, Common_memberAdmin)

admin.site.register(common_member_star, Commmon_menber_starAdmin)

admin.site.register(follower_pair,followers_Adim)

admin.site.register(section_follow_pair)

admin.site.register(common_member_action_log, User_action_log_Admin)