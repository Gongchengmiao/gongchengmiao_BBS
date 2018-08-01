from django.shortcuts import render, redirect
from article.models import ArticlePost
from section.models import SectionForum
from user.models import common_member_star, common_member, commom_member_watch
from django.urls import reverse
import redis
from django.conf import settings
from django.utils import timezone
import datetime
import functools
from django.utils.safestring import mark_safe
import json


# Create your views here.
def index_shell(request):
    user = request.user
    room_name = 'abc'
    # friends_list = user.followers.all()
    friends_list = common_member.objects.all()

    def new_room_name(user1, user2):
        if user1.username < user2.username:
            return user1.username + user2.username
        else:
            return user2.username + user1.username

    room_name_list = list(map(lambda item: new_room_name(user, item), friends_list))

    context = {
        'user': user,
        'friend_list': friends_list,
        'room_name_json': mark_safe(json.dumps(room_name)),
        'room_name_list': mark_safe(json.dumps(room_name_list)),
    }
    return render(request, "x_whole_demo.html", context)


def index(request):

    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('login'))

    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    articles = ArticlePost.objects.filter(
        pub_date__range=(timezone.now() + datetime.timedelta(days=-1), timezone.now()),
        is_school_info=False,
    )
    total_views = {}
    for article in articles:
        total_views[article] = r.get("article:{}:views".format(article.pid))
    top_ten = sorted(total_views.items(), key=lambda item: item[1], reverse=True)[0:10]
    top_ten_list = functools.reduce(lambda x, y: x.append(y) or x, map(lambda x: x[0], top_ten), [])

    latest_posts = ArticlePost.objects.order_by('-pub_date')[0:10]

    school_info = ArticlePost.objects.filter(is_school_info=True).order_by('-pub_date')[0:10]

    user_watch = commom_member_watch.objects.filter(uid=user).order_by('watch_time')

    block = {}

    for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
        sections = SectionForum.objects.filter(block=i)
        result = []
        temp = []
        for ii, section in enumerate(sections):
            if (ii + 1) % 4:
                temp.append(section)
            else:
                temp.append(section)
                result.append(temp)
                temp = []
            if ii == len(sections) - 1 and temp:
                result.append(temp)
        block[i] = result

    user_star = common_member_star.objects.filter(uid=user).order_by('-star_time')[0: 10]

    watch_result = []
    temp = []
    for i, watch in enumerate(user_watch):
        if (i+1) % 4:
            temp.append(watch)
        else:
            temp.append(watch)
            watch_result.append(temp)
            temp = []
        if i == len(user_watch)-1 and temp:
            watch_result.append(temp)

    # print(watch_result[0][0].section)

    context = {
        'popular_posts': enumerate(top_ten_list),
        'school_info': enumerate(school_info),
        'user_star': enumerate(user_star),
        'user_watches': watch_result,
        'user': user,
        'block': block,
    }

    response = render(request, 'x_BBS_index_demo.html', context)
    return response


def redirect_to_login(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    else:
        return redirect(reverse('index'))
