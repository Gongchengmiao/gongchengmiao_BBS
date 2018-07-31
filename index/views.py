from django.shortcuts import render, redirect
from article.models import ArticlePost
from user.models import common_member_star, common_member
from django.urls import reverse
import redis
from django.conf import settings
from django.utils import timezone
import datetime
import functools


# Create your views here.
def index_shell(request):
    user = request.user

    context = {
        'user': user,

    }
    return render(request, "x_whole_demo.html", context)


def index(request):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    articles = ArticlePost.objects.filter(pub_date__range=(timezone.now()+datetime.timedelta(days=-2), timezone.now()))
    total_views = {}
    for article in articles:
        total_views[article] = r.get("article:{}:views".format(article.pid))
    top_ten = sorted(total_views.items(), key=lambda item: item[1], reverse=True)[0:10]

    top_ten_list = functools.reduce(lambda x, y: x.append(y) or x, map(lambda x: x[0], top_ten), [])

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
