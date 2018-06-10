import datetime

from django.contrib import auth
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from .forms import UserLoginForm, UserRegisterForm
from .models import common_member
from django.core.mail import send_mail


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
                if user.email_status is True:

                    response = redirect(reverse('index'))
                    response.set_cookie('username', username,
                                        expires=datetime.datetime.now()+datetime.timedelta(days=10))
                    passwd = common_member.objects.get(username=username).password
                    response.set_cookie('password', passwd,
                                        expires=datetime.datetime.now() + datetime.timedelta(days=10))

                    auth.login(request, user)
                    return response

                else:
                    return render(request, 'login_demo.html', {
                        'form': form,
                        'email_not_active': True,
                        "title": u'中国科学技术大学BBS登录',
                        'password_is_wrong': False,
                    })
            else:
                return render(request, 'login_demo.html', {
                    'form': form,
                    'password_is_wrong': True,
                    "title": u'中国科学技术大学BBS登录',
                    'email_not_active': False,
                })

        else:

            return render(request, "login_demo.html", {"form": form, "title": u'中国科学技术大学BBS登录'})


# 注册操作实现
def register(request):
    # global new_account
    # 当正常访问时候, 返回register.html的渲染
    if request.method == 'GET':
        form = UserRegisterForm()
        # print(1)
        # send_mail('test_demo_subject', 'test_demo_message', 'paulzh@mail.ustc.edu.cn', ['z1991998920@gmail.com', ])
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
                # print(common_member.objects.filter(username=username))
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

            # 邮箱验证
            hostname = 'roarcannotprogramming.com:8017'
            activation_url = hostname + reverse('verify_user', args=(username, ))
            mail_text = u'To 亲爱的同学: \n\n欢迎您使用瀚海星云, 现在仍然是测试版,' \
                        u' 若发现漏洞请联系此邮箱\n\n\n\n您的验证网址为\n\n\n\n\n'+activation_url+'\n\n\n\n\n\n\n\n'\
                        u'From 攻城喵团队'
            send_mail(u'瀚海星云-邮箱验证', mail_text, 'paulzh@mail.ustc.edu.cn', [email, ])

            new_account = common_member()
            new_account.username = username
            new_account.password = make_password(password)
            new_account.email = email
            new_account.save()

            # 需要加入邮箱验证
            return render(request, "register.html", {
                "form": form,
                "title": u"欢迎注册翰海星云BBS",
                "success": True,
            })
        else:
            return render(request, "register.html", {"form": form, "title": u"欢迎注册瀚海星云BBS", "error_unknown": True})

            # issue 1: 用户名首字母大写


# 邮箱验证界面
def email_active(request, username):
    if request.method == 'GET':
        user = common_member.objects.get(username=username)
        if user and user.is_active:
            if user.email_status:
                return render(request, "active_email.html", {"has_verified": True, "title": u"翰海星云用户验证"})  # 已经验证通过了
            else:
                # 现在正在验证
                user.email_status = True
                user.save()
                return render(request, "active_email.html", {"succeed_verified": True, "title": u"翰海星云用户验证"})
        else:
            # 当前用户不存在
            return render(request, "active_email.html", {"user_not_exist": True, "title": u"翰海星云用户验证"})

