from django import forms


# 用户登入表单
class UserLoginForm(forms.Form):
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
                "placeholder": u"用户名",
                "class": "form-control",
            }
        ),
        max_length=20,
        min_length=6,
    )

    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={
            "required": u"请输入密码",
            "max_length": u"密码最长为20位",
            "min_length": u"密码最短位6位",
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": u"密码",
                "class": "form-control",
            }
        ),
        max_length=20,
        min_length=6,
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码必须正确填写")
        else:
            cleaned_data = super(UserLoginForm, self).clean()


# 用户注册表单
class UserRegisterForm(forms.Form):
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

    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={
            "required": u"请输入密码",
            "max_length": u"密码最长为20位",
            "min_length": u"密码最短位6位",
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": u"请输入密码",
                "class": "form-control",
            }
        ),
        max_length=20,
        min_length=6,
    )

    password_confirm = forms.CharField(
        required=True,
        label=u'确认密码',
        error_messages={
            "required": u"请输入密码",
            "max_length": u"密码最长为20位",
            "min_length": u"密码最短位6位",
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": u"请再次输入密码",
                "class": "form-control",
            }
        ),
        max_length=20,
        min_length=6,
    )

    email = forms.EmailField(
        required=True,
        label=u'邮箱',
        error_messages={
            "required": u"请输入邮箱",
        },
        widget=forms.EmailInput(
            attrs={
                "placeholder": u"请输入邮箱",
                "class": "form-control",
            }
        ),
    )

    confirm_message = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(),
    )
