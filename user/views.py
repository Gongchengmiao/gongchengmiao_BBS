import datetime

from django.contrib import auth
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now

from .forms import UserLoginForm, UserRegisterForm, UserPswdGetBackForm, UserChangePSWDForm
from .models import common_member, common_member_email_send_time
from django.core.mail import send_mail, EmailMultiAlternatives, BadHeaderError, EmailMessage
from .tasks import send_email_1
from .tokens import account_activation_token, pswd_get_back_token


# 登入操作实现
def login(request):
    # 如果当前已有用户登入, 则直接跳转到主页
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    # 当正常访问时, 返回login.html的渲染
    if request.method == 'GET':

        form = UserLoginForm()
        return render(request, "login_v2_demo.html", {"form": form, "title": u'中国科学技术大学BBS登录'})
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
                    # response.set_cookie('username', username,
                    #                     expires=datetime.datetime.now()+datetime.timedelta(days=10))
                    # passwd = common_member.objects.get(username=username).password
                    # response.set_cookie('password', passwd,
                    #                     expires=datetime.datetime.now() + datetime.timedelta(days=10))

                    auth.login(request, user)
                    return response

                else:
                    return render(request, 'login_v2_demo.html', {
                        'form': form,
                        'email_not_active': True,
                        "title": u'中国科学技术大学BBS登录',
                        'password_is_wrong': False,
                    })
            else:
                return render(request, 'login_v2_demo.html', {
                    'form': form,
                    'password_is_wrong': True,
                    "title": u'中国科学技术大学BBS登录',
                    'email_not_active': False,
                })

        else:

            return render(request, "login_v2_demo.html", {"form": form, "title": u'中国科学技术大学BBS登录'})


# 注册操作实现
def register(request):
    # global new_account
    # 当正常访问时候, 返回register.html的渲染
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request, "register_demo_v2.html", {"form": form, "title": u"欢迎注册瀚海星云BBS"})
    else:
        # 当提交表单时, 判断用户名是否被注册, 密码是否合法, 再次输入密码是否正确, 是否勾选阅读用户协议
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            email = form.cleaned_data['email']
            confirm_message = form.cleaned_data['confirm_message']

            if common_member.objects.filter(username=username):
                return render(request, "register_demo_v2.html", {
                    "form": form,
                    "title": u"欢迎注册瀚海星云BBS",
                    "user_name_used": True,
                })

            try:
                password_validation.validate_password(password, username)
            except ValidationError as err:
                # print(4)
                error = err
                return render(request, "register_demo_v2.html", {
                    "form": form,
                    "title": u"欢迎注册瀚海星云BBS",
                    "password_invalidate": True,
                    "error_msg": error
                })

            if password != password_confirm:
                return render(request, "register_demo_v2.html", {
                    "form": form,
                    "title": u"欢迎注册瀚海星云BBS",
                    "pw_confirm_error": True,
                })

            if confirm_message is False:
                return render(request, "register_demo_v2.html", {
                    "form": form,
                    "title": u"欢迎注册瀚海星云BBS",
                    "not_confirmed": True,
                })

            new_account = common_member()
            new_account.username = username
            new_account.password = make_password(password)
            new_account.email = email
            new_account.save()

            # token = account_activation_token.make_token(new_account)

            # return render(request, "register.html", {
            #     "form": form,
            #     "title": u"欢迎注册翰海星云BBS",
            #     "waiting": True,
            # })

            return redirect(reverse('wait_email', args=(username, )))

            # 邮箱验证
            # hostname = 'roarcannotprogramming.com:8017'
            # activation_url = hostname + reverse('verify_user', args=(username, ))
            # mail_text = u'<p>To 亲爱的同学:</p> <br/> <br/> <p>欢迎您使用瀚海星云, 现在仍然是测试版,' \
            #             u' 若发现漏洞请联系此邮箱</p> <br/><br/><p>您的验证网址
            # 为</p><br/><br/><br/><a href="'+activation_url+'">'+activatio
            # n_url+'</a><br/><br/><br/><br/><br/><br/>'\
            #             u'<p>From 攻城喵团队</p>'
            # msg = EmailMultiAlternatives(u'瀚海星云-邮箱验证', mail_text, 'paulzh@mail.ustc.edu.cn', [email, ])
            # msg.content_subtype = "html"
            #
            # try:
            #     msg.send()
            # except BadHeaderError:
            #     new_account.delete()
            #     return render(request, "register.html", {"form": form, "title": u"欢迎注册瀚海星云
            # BBS", "error_unknown": True})
            #
            # return render(request, "register.html", {
            #     "form": form,
            #     "title": u"欢迎注册翰海星云BBS",
            #     "success": True,
            # })
        else:
            return render(request, "register_demo_v2.html", {"form": form, "title": u"欢迎注册瀚海星云BBS", "error_unknown": True})

            # issue 1: 用户名首字母大写


# 邮箱验证界面
def email_active(request, uidb64, token):
    if request.method == 'GET':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = common_member.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, common_member.DoesNotExist):
            user = None
        # user = common_member.objects.get(username=username)

        # if user is not None and account_activation_token.check_token(user, token):
        if user is not None and user.is_active and account_activation_token.check_token(user, token):
            # 验证是否超时
            try:
                email_record = common_member_email_send_time.objects.filter(user=user).order_by('-last_send_time')
                email_record = email_record[0]
                # print(str(email_record.last_send_time), str(datetime.datetime.now() + datetime.timedelta(hours=-3)))
                if str(email_record.last_send_time) < str(datetime.datetime.now() + datetime.timedelta(hours=-3)):
                    user.delete()
                    return render(request, "active_email.html", {"title": u"翰海星云用户验证", "time_more": True, })  # 超过验证时间
            except IndexError:
                return render(request, "active_email.html", {"title": u"翰海星云用户验证", "never_send": True, })  # 没发过邮件

            # 邮箱验证
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


# 注册跳转发送邮箱界面
def jump_to_wait(request, username):
    # 只有没有通过验证　并且　距离上次发送邮件时间超过３小时的才能再次发送邮件
    if request.method == 'GET':
        # try:
            # user = common_member.objects.get(username=username)
        user = get_object_or_404(common_member, username=username)
        # except ObjectDoesNotExist:

        email = user.email
        email_status = user.email_status
        new_account = user

        # 查询是否已经验证通过
        if email_status:
            return render(request, "wait_email.html", {"title": u"瀚海星云注册邮件认证", "identified": True, })

        # 查询是否发过邮件
        try:
            email_status = common_member_email_send_time.objects.filter(user=user).order_by('-last_send_time')
            # print(email_status)
            email_status = email_status[0]
            if str(email_status.last_send_time) > str(datetime.datetime.now() + datetime.timedelta(hours=-3)):
                # print(str(email_status.last_send_time), str(datetime.datetime.now() + datetime.timedelta(hours=-3)))

                # 间隔时间小于三小时, 返回'请等待三小时'
                return render(request, "wait_email.html", {"title": u"瀚海星云注册邮件认证", "time_less": True, })
        except IndexError:  # 从未发送过
            pass

        # 配置并发送邮件
        # hostname = 'roarcannotprogramming.com:8017'
        # activation_url = hostname + reverse('verify_user', args=(username,))
        # mail_text = u'<p>To 亲爱的同学:</p> <br/> <br/> <p>欢迎您使用瀚海星云, 现在仍然是测试版,' \
        #             u' 若发现漏洞请联系此邮箱</p> <br/><br/><p>您的验证网' \
        #             u'址为</p><br/><br/><br/><a href="' + activation_url + '">' \
        #             + activation_url +\
        #             '</a><br/><br/><br/><br/><br/><br/>' \
        #             u'<p>From 攻城喵团队</p>'

        current_site = get_current_site(request)
        mail_message = render_to_string('email_message.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': bytes.decode(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': account_activation_token.make_token(user),
        })

        # msg = EmailMultiAlternatives(u'瀚海星云-邮箱验证', mail_text, 'paulzh@mail.ustc.edu.cn', [email, ])
        # msg.content_subtype = "html"

        msg = EmailMessage(
            u'瀚海星云-邮箱验证', mail_message, to=[email, ]
        )

        try:
            # msg.send()
            send_email_1.delay(msg)

        except BadHeaderError:
            new_account.delete()
            return render(request, "wait_email.html", {"title": u"瀚海星云注册邮件认证", "head_wrong": True, })

        # 更新表
        email_record, created = common_member_email_send_time.objects.get_or_create(user=user)
        # email_record.user = user
        email_record.email_time += 1
        email_record.save()

        return render(request, "wait_email.html", {
            "title": u"瀚海星云注册邮件认证",
            "success": True,
        })

    else:
        return render(request, "wait_email.html", {"title": u"瀚海星云注册邮件认证", "method_wrong": True, })


# 登出
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect(reverse('login'))


# 找回密码
def pswdgetback(request):
    if request.method == 'GET':
        # 正常访问
        form = UserPswdGetBackForm()
        return render(request, 'password_getback_demo.html', {'form': form, })
    else:
        # 提交表单
        form = UserPswdGetBackForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = common_member.objects.get(username=username)
            if user.email != email:
                # 用户名或者邮箱错误
                return render(request, "password_getback_demo.html", {'form': form, 'email_or_username_wrong': True, })
            if not user.email_status:
                # 邮箱未被激活
                return render(request, "password_getback_demo.html", {'form': form, 'email_status_error': True, })
            return redirect(reverse('pswdgetback_jump', args=(username, )))
        else:
            # 表单不合法
            return render(request, "password_getback_demo.html", {'form': form, 'message_wrong': True})


# 找回密码发送邮件跳转界面
def pswdgetback_jump(request, username):
    # 只有没有通过验证　并且　距离上次发送邮件时间超过３小时的才能再次发送邮件
    if request.method == 'GET':
        user = get_object_or_404(common_member, username=username)
        email = user.email
        # 查询是否发过邮件
        try:
            email_status = common_member_email_send_time.objects.filter(user=user).order_by('-last_send_time')
            # print(email_status)
            email_status = email_status[0]
            if str(email_status.last_send_time) > str(datetime.datetime.now() + datetime.timedelta(hours=-3)):
                # print(str(email_status.last_send_time), str(datetime.datetime.now() + datetime.timedelta(hours=-3)))

                # 间隔时间小于三小时, 返回'请等待三小时'
                return render(request, "pswd_get_back_jump.html", {"title": u"瀚海星云找回密码邮件认证",
                                                                   "time_less": True, })
        except IndexError:  # 从未发送过
            pass

        # 配置并发送邮件
        current_site = get_current_site(request)
        mail_message = render_to_string('email_message_pswd_getback.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': bytes.decode(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': pswd_get_back_token.make_token(user),
        })

        msg = EmailMessage(
            u'瀚海星云-邮箱找回', mail_message, to=[email, ]
        )

        try:
            # 异步发送
            send_email_1.delay(msg)

        except BadHeaderError:
            return render(request, "pswd_get_back_jump.html", {"title": u"瀚海星云注册邮件认证", "head_wrong": True, })

        # 更新表
        email_record, created = common_member_email_send_time.objects.get_or_create(user=user)
        email_record.email_time += 1
        email_record.save()

        return render(request, "pswd_get_back_jump.html", {
            "title": u"瀚海星云注册邮件认证",
            "success": True,
        })

    else:
        return render(request, "pswd_get_back_jump.html", {"title": u"瀚海星云注册邮件认证", "method_wrong": True, })

    
# 找回密码界面
# 应补充: 一个链接完成后页面失效
def pswd_get_back_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = common_member.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, common_member.DoesNotExist):
        user = None

    if request.method == 'GET':
        if user is not None and user.is_active and pswd_get_back_token.check_token(user, token):
            # 验证是否超时
            try:
                email_record = common_member_email_send_time.objects.filter(user=user).order_by('-last_send_time')
                email_record = email_record[0]

                if str(email_record.last_send_time) < str(datetime.datetime.now() + datetime.timedelta(hours=-3)):

                    return render(request, "error_messages.html", {"title": u"翰海星云错误消息", "time_more": True, })  # 超过验证时间
            except IndexError:
                return render(request, "error_messages.html", {"title": u"翰海星云用户错误消息", "never_send": True, })  # 没发过邮件

            form = UserChangePSWDForm()
            return render(request, "pswd_change_demo.html", {"form": form, "title": u"翰海星云修改密码"})  # 发送密码找回界面
        else:
            # 当前用户不存在
            return render(request, "error_messages.html", {
                            "title": u"翰海星云用户错误消息",
                            "user_not_exist": True,
                            }
                          )

    else:  # method == 'POST'
        form = UserChangePSWDForm(request.POST)
        if form.is_valid():
            # username = request.POST.get('new_pswd', '')
            new_pswd = form.cleaned_data['new_pswd']
            new_pswd_confirm = form.cleaned_data['new_pswd_confirm']

            try:
                password_validation.validate_password(new_pswd, user.username)
            except ValidationError as err:
                error = err
                return render(request, "pswd_change_demo.html", {
                    "form": form,
                    "title": u"翰海星云修改密码",
                    "password_invalidate": True,
                    "error_msg": error
                })

            if new_pswd != new_pswd_confirm:
                return render(request, "pswd_change_demo.html", {"title": u"翰海星云修改密码",
                                                                 "form": form,
                                                                 "confirm_error": u"两次密码输入不一致"})

            user.password = make_password(new_pswd)
            user.save()

            return render(request, "pswd_change_demo.html", {
                "title": u"翰海星云修改密码",
                "form": form,
                "success": True
            })

        else:
            return render(request, "pswd_change_demo.html", {
                "title": u"翰海星云修改密码",
                "form": form,
                "error_unknown": True
            })






