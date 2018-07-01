from django import forms



class UserInfoChangeForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={
            "required": u"请输入用户名",
            "max_length": u"用户名最长为20位",
            "min_length": u"用户名最短位6位",
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": u"请输入用户名",
                "class": "form-control",
            }
        ),
        max_length=20,
        min_length=6,
    )
    portrait = forms.ImageField(required=False, label='edit_portrait',widget=forms.ClearableFileInput())

    gender_choices = (('m','男'),('f','女'))
    gender = forms.ChoiceField(required=True,choices=gender_choices, label='gender')
    show_gender = forms.BooleanField(required=False,label='show_gender')

    profile = forms.CharField(
        required=False,
        label=u"个性签名",
        error_messages={
            "max_length": u"最长为280位",
            "min_length": u"最短位0位",
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": u"个性签名",
                "class": "form-control",
            }
        ),
        max_length=280,
        min_length=0,
    )



