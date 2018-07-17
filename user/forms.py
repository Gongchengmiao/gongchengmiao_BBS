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
                # "class": "form-control",
                "class": "form-control uname"
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
                # "class": "form-control",
                "class": "form-control pword m-b"
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
                "class": "form-control uname",
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
                "class": "form-control pword m-b",
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
                "class": "form-control pword m-b",
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
                "class": "form-control uname",
            }
        ),
    )

    confirm_message = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(),
    )


# 用户找回密码表单
class UserPswdGetBackForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u'用户名',
        error_messages={
            "required": u"请输入用户名",
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": u"请输入用户名",
                "class": "form-control uname",
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
                "class": "form-control uname",
            }
        ),
    )


# 用户修改密码表单
class UserChangePSWDForm(forms.Form):

    new_pswd = forms.CharField(
        required=True,
        label=u'新密码',
        error_messages={
            'required': u'请输入新密码',
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": u"请输入新密码",
                "class": "form-control pword m-b",
            }
        ),
    )

    new_pswd_confirm = forms.CharField(
        required=True,
        label=u'确认密码',
        error_messages={
            'required': u'请确认密码',
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": u"请确认密码",
                "class": "form-control pword m-b",
            }
        ),
    )
