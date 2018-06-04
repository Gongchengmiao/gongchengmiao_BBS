from django.shortcuts import render
from article.models import forum_post, forum_school_info
from user.models import common_member_star
import datetime

# Create your views here.


def index(request):
    popular_posts = forum_post.objects.order_by('-pub_date')[0:10]
    school_info = forum_school_info.objects.order_by('-pub_date')[0:10]
    user_star = common_member_star.objects.filter(uid__username
                                                  =request.COOKIES['username']).order_by('-star_time')[0: 10]

    context = {
        'latest_posts': enumerate(popular_posts),
        'school_info': enumerate(school_info),
        'user_star': enumerate(user_star),
    }

    # return render(request, 'BBS_index_demo.html', context)
    response = render(request, 'BBS_index_demo.html', context)
    # 假设Cookie是z19919998920 为了测试
    response.set_cookie('username', 'z1991998920', expires=datetime.datetime.now()+datetime.timedelta(days=365))
    return response
