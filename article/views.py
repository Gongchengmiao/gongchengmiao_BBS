from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ArticlePostForm, CommentForm
from .models import ArticleColumn, ArticlePost, Comment
from user.models import common_member_action_log
import redis
from django.conf import settings

from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from article.models import ArticlePost

import json
# Create your views here.
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

@login_required(login_url='/login')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            #try:
            new_article = ArticlePost()
            new_article.author = request.user
            new_article.title = cd.get('title')
            new_article.ueditor_body = cd.get('content')
            new_article.save()

            # 更新用户动态
            new_action = common_member_action_log()
            new_action.uid = request.user
            new_action.pid = new_article
            new_action.action = 'post'
            new_action.save()

            #url = reverse('')
            url = reverse('article_detail', kwargs={'pid':new_article.pid,'slug':new_article.slug})
            #print(url)
            return HttpResponseRedirect(url)
                #return HttpResponse('1')
            #except:
                #return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        return render(request, "x_fatie_demo.html", {"article_post_form":article_post_form})

@login_required(login_url='/login')
@csrf_exempt
def article_detail(request, pid, slug):
    article = get_object_or_404(ArticlePost, pid=pid, slug=slug)
    total_views = r.incr("article:{}:views".format(article.pid))
    author = article.author

    all_comments = Comment.objects.filter(article=article).all()

    paginator = Paginator(all_comments, 10)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        comments = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        comments = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        comments = current_page.object_list



    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            new_comment = Comment()
            new_comment.commentator = request.user
            new_comment.article = article
            new_comment.ueditor_body = cd.get('comment_body')
            new_comment.commentator = request.user
            new_comment.counter = article.comment_counter + 1
            article.comment_counter = article.comment_counter + 1
            article.save()
            new_comment.save()
            url = reverse('article_detail', kwargs={'pid': article.pid, 'slug': article.slug})

            return HttpResponseRedirect(url)
    else:
        comment_form = CommentForm()
    return render(request, "x_huitie_demo.html", {"article":article, "comment_form":comment_form, "author":author, "comments":comments, "page":current_page, "total_views":total_views})


@csrf_exempt
@require_POST
@login_required(login_url='/login/')
def like_article(request):
    article_pid = request.POST.get("pid")    #①
    action = request.POST.get("action")    #②
    if article_pid and action:
        try:
            article = ArticlePost.objects.get(pid=article_pid)
            if action=="like":
                article.users_like.add(request.user)    #③
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)    #④
                return HttpResponse("2")
        except:
            return HttpResponse("no")



@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        article = get_object_or_404(ArticlePost, slug=slug)

        if article.likes.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            article.likes.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a company
            article.likes.add(user)
            message = 'You liked this'

    ctx = {'likes_count': article.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')