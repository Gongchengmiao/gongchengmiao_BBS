from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import SectionForum
from .forms import FastPostForm
from article.models import ArticlePost
from user.models import section_follow_pair, commom_member_watch, common_member_action_log, common_member
from django.http import HttpResponse, JsonResponse
import math
# Create your views here.

Num_per_page = 5  # 每页帖子数


@login_required(login_url='/login/')
@csrf_exempt
def section_all(request, section_slug):
    section = SectionForum.objects.filter(slug=section_slug).first()
    posts = ArticlePost.objects.filter(section_belong_fk=section).order_by('-pub_date')[0:2*Num_per_page]
    post_num = ArticlePost.objects.filter(section_belong_fk=section).count()

    if request.method == "POST":
        post_form = FastPostForm(data=request.POST)
        if post_form.is_valid():
            cd = post_form.cleaned_data
            #try:
            new_article = ArticlePost()
            new_article.author = request.user
            new_article.title = cd.get('title')
            new_article.ueditor_body = cd.get('content')
            new_article.section_belong_fk = section
            new_article.save()

            # 更新用户动态
            new_action = common_member_action_log()
            new_action.uid = request.user
            new_action.pid = new_article
            new_action.action = 'post'
            new_action.save()

            common_member.objects.filter(id=request.user.id).update(posts=request.user.posts + 1)

    form = FastPostForm()

    context = {
        'section': section,
        'post_num': post_num,
        'posts': posts,
        'form': form,
    }
    return render(request, 'x_bankuai_demo.html', context)


@login_required(login_url='/login/')
def section_open_posts_list(request):
    # print("what")
    sec_slug = request.GET.get("sec_slug")
    section = SectionForum.objects.filter(slug=sec_slug).first()
    page = request.GET.get("page")  # present active page button
    if request.GET.get("isElite") == '0':
        posts = ArticlePost.objects.filter(section_belong_fk=section).order_by('-pub_date')[Num_per_page*(page-1): Num_per_page*page]
        post_num = ArticlePost.objects.filter(section_belong_fk=section).count()
    else:
        posts = ArticlePost.objects.filter(section_belong_fk=section, isElite=True).order_by('-pub_date')[Num_per_page*(page-1): Num_per_page*page]
        post_num = ArticlePost.objects.filter(section_belong_fk=section, isElite=True).count()
    page_num = math.ceil(post_num/Num_per_page)
    if page == '':
        page = '1'
    page = int(page)

    if request.GET.get('isDecPage') == '1':
        page = max(page-1, 1)
    elif request.GET.get('isIncPage') == '1':
        page = min(page+1,page_num)

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
    test = section_follow_pair.objects.filter(section=section, user=request.user).all()
    if test:
        return JsonResponse({'info': '已经关注', 'num': ''})
    new_pair = section_follow_pair()
    new_pair.user = request.user
    new_pair.section = section
    new_pair_zh_def = commom_member_watch()
    new_pair_zh_def.uid = request.user
    new_pair_zh_def.section = section
    section.follower_num += 1
    new_pair.save()
    new_pair_zh_def.save()
    section.save()
    return JsonResponse({'info': '关注成功', 'num': str(section.follower_num)})
