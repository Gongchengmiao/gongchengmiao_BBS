from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SectionForum
from article.models import ArticlePost
from user.models import section_follow_pair
from django.http import HttpResponse, JsonResponse
import math
# Create your views here.

Num_per_page = 5


@login_required(login_url='/login/')
def section_all(request, section_slug):
    section = SectionForum.objects.filter(slug=section_slug).first()
    posts = ArticlePost.objects.filter(section_belong_fk=section).order_by('-pub_date')[0:2*Num_per_page]
    post_num = ArticlePost.objects.filter(section_belong_fk=section).count()
    context = {
        'section': section,
        'post_num': post_num,
        'posts': posts,
    }
    return render(request, 'x_bankuai_demo.html', context)


@login_required(login_url='/login/')
def section_open_posts_list(request):
    # print("what")
    sec_slug = request.GET.get("sec_slug")
    section = SectionForum.objects.filter(slug=sec_slug).first()
    page = request.GET.get("page")  # present active page button
    post_num = ArticlePost.objects.filter(section_belong_fk=section).count()
    page_num = math.ceil(post_num/Num_per_page)
    if page == '':
        page = '1'
    page = int(page)

    if request.GET.get('isDecPage') == '1':
        page = max(page-1, 1)
    elif request.GET.get('isIncPage') == '1':
        page = min(page+1,page_num)

    if request.GET.get("isElite") == '0':
        posts = ArticlePost.objects.filter(section_belong_fk=section).order_by('-pub_date')[Num_per_page*(page-1): Num_per_page*page]
    else:
        posts = ArticlePost.objects.filter(section_belong_fk=section, isElite=True).order_by('-pub_date')[Num_per_page*(page-1): Num_per_page*page]

    # find the pages to display
    pages_to_show = []
    start = max(min(page - 3, page_num-6), 1)
    end = min(max(page + 3, 7), page_num)
    for pa in range(start, end+1):
        pages_to_show.append(str(pa))

    post_list = []
    for po in posts:
        item = {}
        item = item.fromkeys(('pub_date', 'author', 'author_url', 'url', 'title'))
        item['author_url'] = po.author.get_url()
        item['pub_date'] = po.pub_date.strftime('%a %d/%m/%y')
        item['author'] = po.author.username
        item['url'] = po.get_url()
        item['title'] = po.title
        item['isElite'] = str(po.isElite)
        post_list.append(item)

    context = {
        'pages_to_show': pages_to_show,
        'page_active': str(page),
        'post_list': post_list
    }

    return JsonResponse(context)


@login_required(login_url='/login/')
def section_follow(request):
    sec_slug = request.GET.get('section_slug')
    section = SectionForum.objects.filter(slug=sec_slug).first()
    test= section_follow_pair.objects.filter(section=section, user=request.user).all()
    if test:
        return HttpResponse('已经关注')
    new_pair = section_follow_pair()
    new_pair.user = request.user
    new_pair.section = section
    section.follower_num += 1
    new_pair.save()
    section.save()
    return HttpResponse('关注成功~')
