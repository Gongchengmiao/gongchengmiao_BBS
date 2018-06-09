import datetime

from django.contrib import auth
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .forms import UserLoginForm, UserRegisterForm
from .models import common_member


# 登入操作实现
def login(request):
    # 当正常访问时, 返回login.html的渲染
    # print(1)
    if request.method == 'GET':

        form = UserLoginForm()
        return render(request, "login_demo.html", {"form": form, "title": u'中国科学技术大学BBS登录'})
    else:

        # 当提交表单时, 判断用户名密码是否正确，正确则返回主页的渲染
        # 不正确则返回错误报告
        form = UserLoginForm(request.POST)
        # print(1)
        if form.is_valid():

            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            # print(username, password)

            if user is not None and user.is_active:

                # 加密
                # usrnm = hashlib.md5('zhanghaodashuaibi'.encode('utf-8'))
                # usrnm.update(username.encode('utf-8'))
                # pswd = hashlib.md5('madalaotaiqiangle'.encode('utf-8'))
                # pswd.update(password.encode('utf-8'))

                response = redirect("/")
                response.set_cookie('username', username,
                                    expires=datetime.datetime.now()+datetime.timedelta(days=10))
                passwd = common_member.objects.get(username=username).password
                response.set_cookie('password', passwd,
                                    expires=datetime.datetime.now() + datetime.timedelta(days=10))

                auth.login(request, user)
                return response
            else:
                return render(request, 'login_demo.html', {'form': form, 'password_is_wrong': True})

        else:

            return render(request, "login_demo.html", {"form": form, "title": u'中国科学技术大学BBS登录'})


# 注册操作实现
def register(request):
    # 当正常访问时候, 返回register.html的渲染
    if request.method == 'GET':
        form = UserRegisterForm()
        # print(1)
        return render(request, "register.html", {"form": form, "title": u"欢迎注册瀚海星云BBS"})
    else:
        # 当提交表单时, 判断用户名是否被注册, 密码是否合法, 再次输入密码是否正确, 是否勾选阅读用户协议
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            email = form.cleaned_data['email']
            confirm_message = form.cleaned_data['confirm_message']
            # print(2)

            if common_member.objects.filter(username=username):
                # print(3)
                print(common_member.objects.filter(username=username))
                return render(request, "register.html", {
                    "form": form,
                    "title": u"欢迎注册瀚海星云BBS",
                    "user_name_used": True,
                })

            try:
                password_validation.validate_password(password, username)
            except ValidationError as err:
                # print(4)
                error = err
                return render(request, "register.html", {
                    "form": form,
                    "title": u"欢迎注册瀚海星云BBS",
                    "password_invalidate": True,
                    "error_msg": error
                })

            if password != password_confirm:
                # print(5)
                return render(request, "register.html", {
                    "form": form,
                    "title": u"欢迎注册瀚海星云BBS",
                    "pw_confirm_error": True,
                })

            if confirm_message is False:
                # print(6)
                return render(request, "register.html", {
                    "form": form,
                    "title": u"欢迎注册瀚海星云BBS",
                    "not_confirmed": True,
                })

            new_account = common_member()
            new_account.username = username
            new_account.password = make_password(password)  # 需要测试
            new_account.email = email
            new_account.save()

            # 需要加入邮箱验证
            return render(request, "register.html", {
                "form": form,
                "title": u"欢迎注册翰海星云BBS",
                "success": True,
            })

