from django.shortcuts import render, redirect
from article.models import ArticlePost
from user.models import common_member_star, common_member
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.sessions.models import Session
import datetime
import hashlib


# Create your views here.
def index_shell(request):
    user = request.user

    context = {
        'user': user,

    }
    return render(request, "x_whole_demo.html", context)


def index(request):
    popular_posts = ArticlePost.objects.order_by('-pub_date')[0:10]

    user = request.user

    if not user.is_authenticated:
        return redirect(reverse('login'))
    else:
        user_star = common_member_star.objects.filter(uid=user).order_by('-star_time')[0: 10]

    context = {
        'latest_posts': enumerate(popular_posts),
        'school_info': enumerate(popular_posts),
        'user_star': enumerate(user_star),
        'user': user
    }

    response = render(request, 'x_BBS_index_demo.html', context)
    return response


def redirect_to_login(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        return redirect(reverse('index'))
