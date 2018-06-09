from django.shortcuts import render,redirect
from .models import common_member
from .forms import UserLoginForm
from django.contrib import auth
import datetime
import hashlib
from .models import common_member


# 登入操作实现
def login(request):
    # 当正常访问时, 返回login.html的渲染
    # print(1)
    if request.method == 'GET':

        form = UserLoginForm()
        return render(request, "login_demo.html", {"form": form})
    else:

        # 当提交表单时, 判断用户名密码是否正确，正确则返回主页的渲染
        # 不正确则返回错误报告
        form = UserLoginForm(request.POST)
        print(1)
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

            return render(request, "login_demo.html", {"form": form})


# 注册操作实现
# def register(request):
#
#
