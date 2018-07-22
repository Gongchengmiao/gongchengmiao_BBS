from django.shortcuts import render, redirect
from article.models import ArticlePost
from user.models import common_member_star, common_member
from django.urls import reverse
import datetime
import hashlib

# Create your views here.
def index_shell(request):
    return render(request, "x_whole_demo.html", {})


def index(request):

    popular_posts = ArticlePost.objects.order_by('-pub_date')[0:10]
    # try:
    #     # 验证cookie
    #     cookie_usrnm = request.COOKIES['username']
    #     cookie_pswd = request.COOKIES['password']
    #     user = common_member.objects.get(username=cookie_usrnm)
    #     pswd_user = user.password
    #
    #     # print(pswd_user)
    #
    #     if cookie_pswd == pswd_user:
    #         user_star = common_member_star.objects.filter(uid__username=cookie_usrnm).order_by('-star_time')[0: 10]
    #     else:
    #         user_star = []
    # except KeyError:
    #     user_star = []

    user = request.user

    if not user.is_authenticated:
        return redirect(reverse('login'))
    else:
        user_star = common_member_star.objects.filter(uid=user).order_by('-star_time')[0: 10]

    context = {
        'latest_posts': enumerate(popular_posts),
        'school_info': enumerate(popular_posts),
        'user_star': enumerate(user_star),
    }

    response = render(request, 'x_BBS_index_demo.html', context)
    return response


def redirect_to_login(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        return redirect(reverse('index'))
