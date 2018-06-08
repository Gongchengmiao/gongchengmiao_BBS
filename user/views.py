from django.shortcuts import render,redirect
from .models import common_member
from .forms import UserLoginForm
from django.contrib import auth


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
            print(username, password)

            if user is not None and user.is_active:
                auth.login(request, user)

                # return render(request, "BBS_index_demo.html", {})
                return redirect("/")
            else:
                return render(request, 'login_demo.html', {'form': form, 'password_is_wrong': True})

        else:

            return render(request, "login_demo.html", {"form": form})

