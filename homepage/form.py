from django import forms
from user.models import common_member


# class UserInfoChangeForm(forms.Form):
#     username = forms.CharField(
#         required=True,
#         label=u"用户名",
#         error_messages={
#             "required": u"请输入用户名",
#             "max_length": u"用户名最长为20位",
#             "min_length": u"用户名最短位6位",
#         },
#         widget=forms.TextInput(
#             attrs={
#                 "placeholder": u"请输入用户名",
#                 "class": "input-field",
#             }
#         ),
#         max_length=20,
#         min_length=6,
#     )
#     portrait = forms.ImageField(
#         required=False,
#         label='edit_portrait',
#         widget=forms.ClearableFileInput(
#             attrs={
#                 "class": "avatar-upload",
#             }
#         )
#     )
#
#     gender_choices = (('m','男'),('f','女'))
#     gender = forms.ChoiceField(
#         required=True,
#         choices=gender_choices,
#         label='gender',
#         widget=forms.RadioSelect()
#     )
#     show_gender = forms.BooleanField(required=False,label='show_gender')
#
#     profile = forms.CharField(
#         required=False,
#         label=u"个性签名",
#         error_messages={
#             "max_length": u"最长为280位",
#             "min_length": u"最短位0位",
#         },
#         widget=forms.Textarea(
#             attrs={
#                 "placeholder": u"我的简介",
#                 "class": "textarea-wrapper",
#             }
#         ),
#         max_length=280,
#         min_length=0,
#     )

class UserInfoChangeForm(forms.ModelForm):
    class Meta:
        model = common_member
        fields = ['username', 'stu_num', 'department', 'gender', 'profile', 'show_gender', 'portrait', 'birthday']
        widgets = {
            'profile': forms.Textarea(
                attrs={
                    "placeholder": u"我的简介",
                    "class": "textarea-wrapper",
                }
            ),
            'gender': forms.RadioSelect(),
            'portrait': forms.FileInput(),
            'username': forms.TextInput(
                attrs={
                    "placeholder": u"请输入用户名",
                    "class": "input-field",
                }
            ),
        }
        required = {
            'portrait': False
        }



